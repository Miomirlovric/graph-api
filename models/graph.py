from typing import List, Literal, Optional

from pydantic import BaseModel


class Edge(BaseModel):
    source: str
    target: str


class GraphRequest(BaseModel):
    nodes: Optional[List[str]] = None
    edges: List[Edge]
    directed: bool = False


GraphType = Literal["default", "dag", "scc"]


class RandomGraphRequest(BaseModel):
    vertex_count: int
    directed: bool = False
    graph_type: GraphType = "default"
