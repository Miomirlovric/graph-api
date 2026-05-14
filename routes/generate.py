from fastapi import APIRouter

from helpers.graph_factory import GraphFactory
from helpers.validators import ValidationChain, VertexCountValidator
from models.graph import RandomGraphRequest
from models.responses import EdgeInfo, GenerateGraphResponse

router = APIRouter(prefix="/graph", tags=["Generate"])


@router.post("/generate", response_model=GenerateGraphResponse)
def generate(req: RandomGraphRequest) -> GenerateGraphResponse:
    """
    Generate a random Erdos-Renyi graph.
    Supply only the number of vertices and whether it should be directed.
    The returned nodes/edges can be passed directly to /analyze/* endpoints.
    """
    ValidationChain([VertexCountValidator(minimum=2, maximum=500)]).run(req)

    G = GraphFactory.random(req)
    is_directed = req.directed or req.graph_type != "default"

    edges = []
    for u, v, data in G.edges(data=True):
        weight = data.get("weight") if req.include_weights else None
        edges.append(EdgeInfo(source=str(u), target=str(v), weight=weight))

    return GenerateGraphResponse(
        directed=is_directed,
        nodes=list(G.nodes),
        edges=edges,
    )
