from fastapi import APIRouter, HTTPException

from helpers.analysis import compute_topological_sort, validate_dag
from helpers.graph_builder import build_directed_graph
from models.graph import GraphRequest
from models.responses import TopologicalSortResponse

router = APIRouter(prefix="/analyze", tags=["Topological Sort"])


@router.post("/topological-sort", response_model=TopologicalSortResponse)
def topological_sort(req: GraphRequest) -> TopologicalSortResponse:
    if not req.edges:
        raise HTTPException(status_code=400, detail="At least one edge is required.")
    G = build_directed_graph(req)
    if error := validate_dag(G):
        raise HTTPException(status_code=422, detail=error)
    return compute_topological_sort(G)
