from fastapi import APIRouter, HTTPException

from helpers.analysis import compute_properties
from helpers.graph_builder import build_graph
from models.graph import GraphRequest
from models.responses import PropertiesResponse

router = APIRouter(prefix="/analyze", tags=["Properties"])


@router.post("/properties", response_model=PropertiesResponse)
def properties(req: GraphRequest) -> PropertiesResponse:
    """
    Return basic graph properties:
    - diameter
    - density  (rounded to 3 decimals)
    - max degree vertex and its value
    """
    if not req.edges:
        raise HTTPException(status_code=400, detail="At least one edge is required.")
    G = build_graph(req)
    return PropertiesResponse(properties=compute_properties(G))
