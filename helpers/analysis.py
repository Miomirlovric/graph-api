"""Graph analysis helpers – each function works on both Graph and DiGraph."""

import math
from typing import Union

import networkx as nx

from models.responses import (
    CentralitiesResult,
    CentralityEntry,
    MaxDegreeEntry,
    PropertiesResult,
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

    try:
        if G.is_directed():
            if nx.is_strongly_connected(G):
                diameter = nx.diameter(G)
            else:
                diameter = nx.diameter(G.to_undirected())
        else:
            if nx.is_connected(G):
                diameter = nx.diameter(G)
            else:
                largest_cc = max(nx.connected_components(G), key=len)
                diameter = nx.diameter(G.subgraph(largest_cc))
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
