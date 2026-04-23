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

    G = generate_random_graph(
        req.vertex_count,
        req.directed,
        req.graph_type,
        req.include_weights,
        req.weight_range,
    )
    is_directed = req.directed or req.graph_type != "default"

    edges = []
    for u, v, data in G.edges(data=True):
        weight = data.get("weight") if req.include_weights else None
        edges.append(EdgeInfo(source=str(u), target=str(v), weight=weight))

    return GenerateGraphResponse(
        directed=is_directed,
        nodes=list(G.nodes),
        edges=edges,
    )
