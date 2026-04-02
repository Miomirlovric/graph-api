from typing import List, Optional

from pydantic import BaseModel


class Edge(BaseModel):
    source: str
    target: str


class GraphRequest(BaseModel):
    nodes: Optional[List[str]] = None
    edges: List[Edge]
    directed: bool = False


class RandomGraphRequest(BaseModel):
    vertex_count: int
    directed: bool = False
