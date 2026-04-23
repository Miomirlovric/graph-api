"""
Typed Pydantic response models for every API endpoint.

All return types are named classes so NSwag / Swagger UI generates
proper TypeScript/C# client types — no anonymous objects.
"""

from typing import Annotated, List, Optional, Tuple

from pydantic import BaseModel, WithJsonSchema

# NSwag-friendly nullable float - generates {"type": "number", "nullable": true}
NullableFloat = Annotated[Optional[float], WithJsonSchema({"type": "number", "nullable": True})]


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
    weight: NullableFloat = None


class GenerateGraphResponse(BaseModel):
    directed: bool
    nodes: List[str]
    edges: List[EdgeInfo]


# ── Topological sort ──────────────────────────────────────────────────

class TopologicalSortResponse(BaseModel):
    order: List[str]


# ── Strongly connected components ─────────────────────────────────────

class SCCComponent(BaseModel):
    vertices: List[str]


class StronglyConnectedComponentsResponse(BaseModel):
    count: int
    largest: SCCComponent


# ── Shortest paths (Dijkstra) ───────────────────────────────────────────

class ShortestPathEntry(BaseModel):
    """Distance and path from source to a single target vertex."""
    vertex: str
    distance: NullableFloat = None
    path: List[str]


class ShortestPathsResponse(BaseModel):
    """Shortest paths from a source vertex to all other vertices."""
    source: str
    paths: List[ShortestPathEntry]
    farthest_vertex: str
    farthest_path: List[str]
