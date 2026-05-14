from fastapi import APIRouter

from helpers.analysis import compute_shortest_paths
from helpers.graph_factory import GraphFactory
from helpers.route_handler import execute_analysis
from helpers.validators import (
    EdgesExistValidator,
    NonNegativeWeightsValidator,
    SourceVertexExistsValidator,
)
from models.graph import ShortestPathsRequest
from models.responses import ShortestPathsResponse

router = APIRouter(prefix="/graph/analyze", tags=["Shortest Paths"])


@router.post("/shortest-paths", response_model=ShortestPathsResponse)
def shortest_paths(req: ShortestPathsRequest) -> ShortestPathsResponse:
    return execute_analysis(
        req,
        pre_build_validators=[
            EdgesExistValidator(),
            NonNegativeWeightsValidator(),
        ],
        graph_builder=GraphFactory.undirected_from_shortest_paths,
        post_build_validators=[SourceVertexExistsValidator(req.source)],
        compute=lambda G, r: compute_shortest_paths(G, r.source),
    )
