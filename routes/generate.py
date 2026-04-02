from fastapi import APIRouter, HTTPException

from helpers.graph_builder import generate_random_graph
from models.graph import RandomGraphRequest
from models.responses import EdgeInfo, GenerateGraphResponse

router = APIRouter(prefix="/graph", tags=["Generate"])


@router.post("/generate", response_model=GenerateGraphResponse)
def generate(req: RandomGraphRequest) -> GenerateGraphResponse:
    """
    Generate a random Erdos-Renyi graph.
    Supply only the number of vertices and whether it should be directed.
    The returned nodes/edges can be passed directly to /analyze/* endpoints.
    """
    if req.vertex_count < 2:
        raise HTTPException(status_code=400, detail="vertex_count must be at least 2.")
    if req.vertex_count > 500:
        raise HTTPException(status_code=400, detail="vertex_count must be at most 500.")

    G = generate_random_graph(req.vertex_count, req.directed)
    return GenerateGraphResponse(
        directed=req.directed,
        nodes=list(G.nodes),
        edges=[EdgeInfo(source=str(u), target=str(v)) for u, v in G.edges],
    )
