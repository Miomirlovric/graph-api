"""Graph analysis helpers – each function works on both Graph and DiGraph."""

import math
from typing import Union

import networkx as nx

from models.responses import (
    CentralitiesResult,
    CentralityEntry,
    MaxDegreeEntry,
    PropertiesResult,
    SCCComponent,
    ShortestPathEntry,
    ShortestPathsResponse,
    StronglyConnectedComponentsResponse,
    TopologicalSortResponse,
)

GraphLike = Union[nx.Graph, nx.DiGraph]


# ── Centralities ─────────────────────────────────────────────────────
def compute_centralities(G: GraphLike) -> CentralitiesResult:
    """Return the vertex/-ices with the highest degree / betweenness / closeness."""
    deg = nx.degree_centrality(G)
    bet = nx.betweenness_centrality(G, normalized=True)
    clo = nx.closeness_centrality(G)

    def _max_items(d: dict) -> CentralityEntry:
        max_val = max(d.values())
        verts = sorted(
            v for v, val in d.items()
            if math.isclose(val, max_val, rel_tol=1e-9, abs_tol=1e-12)
        )
        return CentralityEntry(vertices=verts, value=round(max_val, 3))

    return CentralitiesResult(
        degree=_max_items(deg),
        betweenness=_max_items(bet),
        closeness=_max_items(clo),
    )


# ── Basic properties (diameter, density, max degree) ─────────────────
def compute_properties(G: GraphLike) -> PropertiesResult:
    density = round(nx.density(G), 3)

    # The diameter is only well-defined when the graph is connected (strongly
    # connected, if directed). The route's DiameterComputableValidator rejects
    # graphs that aren't, so by here nx.diameter always returns a true value —
    # The guard below only covers direct callers that bypass the validator.
    try:
        diameter = nx.diameter(G)
    except nx.NetworkXError:
        diameter = 0

    deg = dict(G.degree())
    max_val = max(deg.values())
    max_vertices = sorted(v for v, d in deg.items() if d == max_val)

    return PropertiesResult(
        diameter=diameter,
        density=density,
        max_degree=MaxDegreeEntry(vertices=max_vertices, value=max_val),
    )


# ── Topological sort ──────────────────────────────────────────────────
def validate_dag(G: nx.DiGraph) -> str | None:
    """Return an error message if G is not a DAG, otherwise None."""
    cycle = None
    try:
        cycle = nx.find_cycle(G)
    except nx.NetworkXNoCycle:
        return None
    edge = next(iter(cycle))
    return f"Graph contains a cycle (e.g. {edge[0]} → {edge[1]}): topological sort requires a DAG."


def compute_topological_sort(G: nx.DiGraph) -> TopologicalSortResponse:
    """Return ALL valid topological orderings of a DAG."""
    all_orders = [list(o) for o in nx.all_topological_sorts(G)]
    return TopologicalSortResponse(
        order=all_orders[0],   # first ordering (backward-compat field)
        orders=all_orders,     # full list of valid orderings
    )


# ── Diameter / connectivity ───────────────────────────────────────────
def validate_diameter_computable(G: GraphLike) -> str | None:
    """Return an error message if the graph's diameter is not well-defined.

    The diameter requires every vertex to reach every other vertex:
    a directed graph must be strongly connected, an undirected graph
    must be connected. Otherwise some distances are infinite and the
    diameter (and the rest of the analysis question) is meaningless.
    """
    if G.is_directed():
        if not nx.is_strongly_connected(G):
            return (
                "Directed graph is not strongly connected: the diameter is "
                "undefined because some vertices cannot reach each other. "
                "Add edges so every vertex is reachable from every other vertex."
            )
    elif not nx.is_connected(G):
        return (
            "Graph is not connected: the diameter is undefined because some "
            "vertices cannot reach each other. Add edges so the graph is "
            "connected."
        )
    return None


# ── Strongly connected components ─────────────────────────────────────
def validate_scc_graph(G: nx.DiGraph) -> str | None:
    if all(len(c) == 1 for c in nx.strongly_connected_components(G)):
        return (
            "Graph has no cycles: every vertex is its own SCC. "
            "Add at least one directed cycle so the question is non-trivial."
        )
    return None


def compute_scc(G: nx.DiGraph) -> StronglyConnectedComponentsResponse:
    """Return the number of SCCs and the largest one (most vertices)."""
    components = list(nx.strongly_connected_components(G))
    largest_vertices = sorted(max(components, key=len))
    return StronglyConnectedComponentsResponse(
        count=len(components),
        largest=SCCComponent(vertices=largest_vertices),
    )


# ── Shortest paths (Dijkstra) ───────────────────────────────────────────
def compute_shortest_paths(G: nx.Graph, source: str) -> ShortestPathsResponse:
    distances, paths = nx.single_source_dijkstra(G, source)

    entries: list[ShortestPathEntry] = []
    for vertex in sorted(G.nodes()):
        if vertex == source:
            continue
        dist = distances.get(vertex, float("inf"))
        path = paths.get(vertex, [])
        entries.append(ShortestPathEntry(
            vertex=vertex,
            distance=round(dist, 2),
            path=path,
        ))

    reachable = [(v, d) for v, d in distances.items() if v != source and d < float("inf")]
    if reachable:
        farthest_vertex, _ = max(reachable, key=lambda x: x[1])
        farthest_path = paths[farthest_vertex]
    else:
        farthest_vertex = source
        farthest_path = [source]

    return ShortestPathsResponse(
        source=source,
        paths=entries,
        farthest_vertex=farthest_vertex,
        farthest_path=farthest_path,
    )
