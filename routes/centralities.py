from fastapi import APIRouter, HTTPException

from helpers.analysis import compute_centralities
from helpers.graph_builder import build_graph
from models.graph import GraphRequest
from models.responses import CentralitiesResponse

router = APIRouter(prefix="/analyze", tags=["Centralities"])


@router.post("/centralities", response_model=CentralitiesResponse)
def centralities(req: GraphRequest) -> CentralitiesResponse:
    """
    Return the vertex/-ices with the highest degree / betweenness / closeness
    centrality for the submitted graph. Tied vertices are all returned.
    """
    if not req.edges:
        raise HTTPException(status_code=400, detail="At least one edge is required.")
    G = build_graph(req)
    return CentralitiesResponse(centralities=compute_centralities(G))
