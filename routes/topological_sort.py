from fastapi import APIRouter

from helpers.analysis import compute_topological_sort
from helpers.graph_factory import GraphFactory
from helpers.route_handler import execute_analysis
from helpers.validators import DagValidator, EdgesExistValidator
from models.graph import GraphRequest
from models.responses import TopologicalSortResponse

router = APIRouter(prefix="/analyze", tags=["Topological Sort"])


@router.post("/topological-sort", response_model=TopologicalSortResponse)
def topological_sort(req: GraphRequest) -> TopologicalSortResponse:
    return execute_analysis(
        req,
        pre_build_validators=[EdgesExistValidator()],
        graph_builder=GraphFactory.directed_from_request,
        post_build_validators=[DagValidator()],
        compute=lambda G, _: compute_topological_sort(G),
    )
