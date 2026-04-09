from fastapi import APIRouter, HTTPException

from helpers.analysis import compute_scc, validate_scc_graph
from helpers.graph_builder import build_directed_graph
from models.graph import GraphRequest
from models.responses import StronglyConnectedComponentsResponse

router = APIRouter(prefix="/analyze", tags=["Strongly Connected Components"])


@router.post("/scc", response_model=StronglyConnectedComponentsResponse)
def strongly_connected_components(
    req: GraphRequest,
) -> StronglyConnectedComponentsResponse:
    if not req.edges:
        raise HTTPException(status_code=400, detail="At least one edge is required.")
    G = build_directed_graph(req)
    if error := validate_scc_graph(G):
        raise HTTPException(status_code=422, detail=error)
    return compute_scc(G)
