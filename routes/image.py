from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from helpers.drawing import draw_graph
from helpers.graph_factory import GraphFactory
from helpers.validators import EdgesExistValidator, ValidationChain
from models.graph import GraphRequest

router = APIRouter(prefix="/graph", tags=["Visualisation"])


@router.post("/image")
def graph_image(req: GraphRequest):
    """
    Return a PNG visualisation of the submitted graph.
    Directed graphs are drawn with arrows.
    """
    ValidationChain([EdgesExistValidator()]).run(req)

    G = GraphFactory.from_request(req)
    buf = draw_graph(G)
    return StreamingResponse(buf, media_type="image/png")
