from fastapi import APIRouter, HTTPException

from helpers.analysis import compute_shortest_paths
from helpers.graph_builder import build_graph
from models.graph import GraphRequest, ShortestPathsRequest
from models.responses import ShortestPathsResponse

router = APIRouter(prefix="/graph/analyze", tags=["Shortest Paths"])


@router.post("/shortest-paths", response_model=ShortestPathsResponse)
def shortest_paths(req: ShortestPathsRequest) -> ShortestPathsResponse:
    if not req.edges:
        raise HTTPException(status_code=400, detail="At least one edge is required.")

    # Validate no negative weights
    for e in req.edges:
        if e.weight is not None and e.weight < 0:
            raise HTTPException(
                status_code=400,
                detail=f"Negative weight {e.weight} on edge {e.source}->{e.target}. "
                       "Dijkstra's algorithm requires non-negative weights.",
            )

    # Build undirected graph
    graph_req = GraphRequest(
        nodes=req.nodes,
        edges=req.edges,
        directed=False,  # Force undirected
    )
    G = build_graph(graph_req)

    # Validate source vertex exists
    if req.source not in G.nodes():
        raise HTTPException(
            status_code=400,
            detail=f"Source vertex '{req.source}' not found in graph.",
        )

    return compute_shortest_paths(G, req.source)
