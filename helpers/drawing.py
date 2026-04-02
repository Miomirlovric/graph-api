"""Graph visualisation helper."""

import io
from typing import Union

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

GraphLike = Union[nx.Graph, nx.DiGraph]


def draw_graph(G: GraphLike) -> io.BytesIO:
    is_directed = isinstance(G, nx.DiGraph)

    try:
        pos = nx.kamada_kawai_layout(G)
    except Exception:
        pos = nx.spring_layout(G, seed=42)

    fig, ax = plt.subplots(figsize=(7, 7))

    nx.draw_networkx_nodes(G, pos, ax=ax, node_color="lightblue", node_size=900)
    nx.draw_networkx_labels(G, pos, ax=ax, font_weight="bold", font_size=10)

    if is_directed:
        nx.draw_networkx_edges(
            G, pos, ax=ax,
            edge_color="gray",
            arrows=True,
            arrowsize=18,
            width=1.5,
            connectionstyle="arc3,rad=0.2",
            min_source_margin=20,
            min_target_margin=20,
        )
    else:
        nx.draw_networkx_edges(
            G, pos, ax=ax,
            edge_color="gray",
            width=1.5,
        )

    ax.axis("off")

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", dpi=120)
    plt.close(fig)
    buf.seek(0)
    return buf
