from fastapi import APIRouter

from helpers.analysis import compute_scc
from helpers.graph_factory import GraphFactory
from helpers.route_handler import execute_analysis
from helpers.validators import EdgesExistValidator, SccValidator
from models.graph import GraphRequest
from models.responses import StronglyConnectedComponentsResponse

router = APIRouter(prefix="/analyze", tags=["Strongly Connected Components"])


@router.post("/scc", response_model=StronglyConnectedComponentsResponse)
def strongly_connected_components(
    req: GraphRequest,
) -> StronglyConnectedComponentsResponse:
    return execute_analysis(
        req,
        pre_build_validators=[EdgesExistValidator()],
        graph_builder=GraphFactory.directed_from_request,
        post_build_validators=[SccValidator()],
        compute=lambda G, _: compute_scc(G),
    )
