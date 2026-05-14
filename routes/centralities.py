from fastapi import APIRouter

from helpers.analysis import compute_centralities
from helpers.graph_factory import GraphFactory
from helpers.route_handler import execute_analysis
from helpers.validators import EdgesExistValidator
from models.graph import GraphRequest
from models.responses import CentralitiesResponse

router = APIRouter(prefix="/analyze", tags=["Centralities"])


@router.post("/centralities", response_model=CentralitiesResponse)
def centralities(req: GraphRequest) -> CentralitiesResponse:
    """
    Return the vertex/-ices with the highest degree / betweenness / closeness
    centrality for the submitted graph. Tied vertices are all returned.
    """
    return execute_analysis(
        req,
        pre_build_validators=[EdgesExistValidator()],
        graph_builder=GraphFactory.from_request,
        compute=lambda G, _: CentralitiesResponse(centralities=compute_centralities(G)),
    )
