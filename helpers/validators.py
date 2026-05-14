"""
Validation pipeline (Chain of Responsibility).

Validators are small, single-purpose objects that inspect either the request
or the built graph and raise HTTPException to short-circuit the pipeline.

A ValidationChain runs them in order and stops on the first failure.
"""

from abc import ABC, abstractmethod
from typing import Iterable

from fastapi import HTTPException

import networkx as nx

from helpers.analysis import validate_dag, validate_scc_graph
from models.graph import GraphRequest, RandomGraphRequest, ShortestPathsRequest


class Validator(ABC):
    """One link in the validation chain. Raise HTTPException on failure."""

    @abstractmethod
    def validate(self, target) -> None:  # noqa: ANN001
        ...


class ValidationChain:
    """Composes validators and runs them in order."""

    def __init__(self, validators: Iterable[Validator] | None = None):
        self._validators: list[Validator] = list(validators) if validators else []

    def add(self, validator: Validator) -> "ValidationChain":
        self._validators.append(validator)
        return self

    def run(self, target) -> None:  # noqa: ANN001
        for v in self._validators:
            v.validate(target)


#Request-level validators (run BEFORE the graph is built)


class EdgesExistValidator(Validator):
    """Reject empty edge lists (the universal precondition for analysis routes)."""

    def validate(self, req: GraphRequest) -> None:
        if not req.edges:
            raise HTTPException(
                status_code=400,
                detail="At least one edge is required.",
            )


class NonNegativeWeightsValidator(Validator):
    """Dijkstra and similar require non-negative weights."""

    def validate(self, req: GraphRequest) -> None:
        for e in req.edges:
            if e.weight is not None and e.weight < 0:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Negative weight {e.weight} on edge "
                        f"{e.source}->{e.target}. "
                        "Dijkstra's algorithm requires non-negative weights."
                    ),
                )


class VertexCountValidator(Validator):
    """Bounds check for /graph/generate."""

    def __init__(self, minimum: int, maximum: int):
        self.minimum = minimum
        self.maximum = maximum

    def validate(self, req: RandomGraphRequest) -> None:
        if req.vertex_count < self.minimum:
            raise HTTPException(
                status_code=400,
                detail=f"vertex_count must be at least {self.minimum}.",
            )
        if req.vertex_count > self.maximum:
            raise HTTPException(
                status_code=400,
                detail=f"vertex_count must be at most {self.maximum}.",
            )


#Graph-level validators (run AFTER the graph is built)


class SourceVertexExistsValidator(Validator):
    def __init__(self, source: str):
        self.source = source

    def validate(self, G: nx.Graph) -> None:
        if self.source not in G.nodes():
            raise HTTPException(
                status_code=400,
                detail=f"Source vertex '{self.source}' not found in graph.",
            )


class DagValidator(Validator):
    def validate(self, G: nx.DiGraph) -> None:
        if error := validate_dag(G):
            raise HTTPException(status_code=422, detail=error)


class SccValidator(Validator):
    def validate(self, G: nx.DiGraph) -> None:
        if error := validate_scc_graph(G):
            raise HTTPException(status_code=422, detail=error)
