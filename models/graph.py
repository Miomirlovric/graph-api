from typing import Annotated, List, Literal, Optional, Tuple

from pydantic import BaseModel, Field, WithJsonSchema

# NSwag-friendly nullable float - generates {"type": "number", "nullable": true}
NullableFloat = Annotated[Optional[float], WithJsonSchema({"type": "number", "nullable": True})]


class Edge(BaseModel):
    source: str
    target: str
    weight: NullableFloat = None


class GraphRequest(BaseModel):
    nodes: Optional[List[str]] = None
    edges: List[Edge]
    directed: bool = False


GraphType = Literal["default", "dag", "scc"]


class RandomGraphRequest(BaseModel):
    vertex_count: int
    directed: bool = False
    graph_type: GraphType = "default"
    include_weights: bool = False
    weight_range: Tuple[float, float] = Field(default=(0.1, 2.0))


class ShortestPathsRequest(BaseModel):
    """Request for shortest paths analysis on an undirected weighted graph."""
    nodes: Optional[List[str]] = None
    edges: List[Edge]
    source: str
