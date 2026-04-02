from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from helpers.drawing import draw_graph
from helpers.graph_builder import build_graph
from models.graph import GraphRequest

router = APIRouter(prefix="/graph", tags=["Visualisation"])


@router.post("/image")
def graph_image(req: GraphRequest):
    """
    Return a PNG visualisation of the submitted graph.
    Directed graphs are drawn with arrows.
    """
    if not req.edges:
        raise HTTPException(status_code=400, detail="At least one edge is required.")
    G = build_graph(req)
    buf = draw_graph(G)
    return StreamingResponse(buf, media_type="image/png")
