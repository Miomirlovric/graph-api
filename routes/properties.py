from fastapi import APIRouter

from helpers.analysis import compute_properties
from helpers.graph_factory import GraphFactory
from helpers.route_handler import execute_analysis
from helpers.validators import DiameterComputableValidator, EdgesExistValidator
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
    return execute_analysis(
        req,
        pre_build_validators=[EdgesExistValidator()],
        graph_builder=GraphFactory.from_request,
        post_build_validators=[DiameterComputableValidator()],
        compute=lambda G, _: PropertiesResponse(properties=compute_properties(G)),
    )
