"""
Typed Pydantic response models for every API endpoint.

All return types are named classes so NSwag / Swagger UI generates
proper TypeScript/C# client types — no anonymous objects.
"""

from typing import List, Optional

from pydantic import BaseModel


# ── Health ────────────────────────────────────────────────────────────

class HealthResponse(BaseModel):
    status: str


# ── Centralities ──────────────────────────────────────────────────────

class CentralityEntry(BaseModel):
    """One centrality metric: the tied-top vertices and the shared value."""
    vertices: List[str]
    value: float


class CentralitiesResult(BaseModel):
    degree: CentralityEntry
    betweenness: CentralityEntry
    closeness: CentralityEntry


class CentralitiesResponse(BaseModel):
    centralities: CentralitiesResult


# ── Properties ────────────────────────────────────────────────────────

class MaxDegreeEntry(BaseModel):
    vertices: List[str]
    value: int


class PropertiesResult(BaseModel):
    diameter: int
    density: float
    max_degree: MaxDegreeEntry


class PropertiesResponse(BaseModel):
    properties: PropertiesResult


# ── Random graph generation ───────────────────────────────────────────

class EdgeInfo(BaseModel):
    source: str
    target: str


class GenerateGraphResponse(BaseModel):
    directed: bool
    nodes: List[str]
    edges: List[EdgeInfo]
