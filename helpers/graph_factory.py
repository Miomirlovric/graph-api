from typing import Union

import networkx as nx

from helpers.graph_builder import (
    build_directed_graph,
    build_graph,
    generate_random_graph,
)
from models.graph import GraphRequest, RandomGraphRequest, ShortestPathsRequest

GraphLike = Union[nx.Graph, nx.DiGraph]


class GraphFactory:
    """Centralised constructor for every flavour of graph the API uses."""

    @staticmethod
    def from_request(req: GraphRequest) -> GraphLike:
        """Honour the request's `directed` flag (default behaviour)."""
        return build_graph(req)

    @staticmethod
    def directed_from_request(req: GraphRequest) -> nx.DiGraph:
        """Force a DiGraph regardless of the `directed` flag (DAG, SCC)."""
        return build_directed_graph(req)

    @staticmethod
    def undirected_from_shortest_paths(req: ShortestPathsRequest) -> nx.Graph:
        """Build an undirected graph for Dijkstra (Dijkstra here is undirected)."""
        graph_req = GraphRequest(
            nodes=req.nodes,
            edges=req.edges,
            directed=False,
        )
        return build_graph(graph_req)

    @staticmethod
    def random(req: RandomGraphRequest) -> nx.Graph:
        return generate_random_graph(
            req.vertex_count,
            req.directed,
            req.graph_type,
            req.include_weights,
            req.weight_range,
        )
