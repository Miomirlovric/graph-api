"""Graph visualisation helper."""

import io
from typing import Union

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

GraphLike = Union[nx.Graph, nx.DiGraph]

_NODE_COLOR = "lightblue"
_EDGE_COLOR = "#555555"


def _dag_layout(G: nx.DiGraph) -> dict[str, tuple[float, float]]:
    """Left-to-right layered layout based on topological generations."""
    layers = list(nx.topological_generations(G))
    pos: dict[str, tuple[float, float]] = {}
    for x_idx, layer in enumerate(layers):
        nodes = sorted(layer)
        y_count = len(nodes)
        for y_idx, node in enumerate(nodes):
            y = (y_idx - (y_count - 1) / 2.0) * 2.0
            pos[node] = (x_idx * 3.0, y)
    return pos


def draw_graph(G: GraphLike) -> io.BytesIO:
    is_directed = isinstance(G, nx.DiGraph)
    is_dag = is_directed and nx.is_directed_acyclic_graph(G)

    if is_dag:
        pos = _dag_layout(G)  # type: ignore[arg-type]
        n_layers = len(list(nx.topological_generations(G)))  # type: ignore[arg-type]
        fig_w = max(8, n_layers * 3.0)
        fig_h = max(4, G.number_of_nodes() * 0.8)
        fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    else:
        try:
            pos = nx.kamada_kawai_layout(G)
        except Exception:
            pos = nx.spring_layout(G, seed=42)
        fig, ax = plt.subplots(figsize=(7, 7))

    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=_NODE_COLOR, node_size=1200)
    nx.draw_networkx_labels(G, pos, ax=ax, font_weight="bold", font_size=11)

    if is_directed:
        nx.draw_networkx_edges(
            G, pos, ax=ax,
            edge_color=_EDGE_COLOR,
            arrows=True,
            arrowsize=22,
            width=2.0,
            connectionstyle="arc3,rad=0.0" if is_dag else "arc3,rad=0.15",
            min_source_margin=24,
            min_target_margin=24,
        )
    else:
        nx.draw_networkx_edges(
            G, pos, ax=ax,
            edge_color=_EDGE_COLOR,
            width=2.0,
        )

    # Draw edge weight labels if weights are present (skip weights of 0)
    edge_weights = nx.get_edge_attributes(G, "weight")
    if edge_weights:
        edge_labels = {k: f"{v:.2f}" for k, v in edge_weights.items() if v != 0}
        nx.draw_networkx_edge_labels(
            G, pos, ax=ax,
            edge_labels=edge_labels,
            font_size=9,
            font_color="#333333",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="none", alpha=0.7),
        )

    ax.axis("off")

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", dpi=150)
    plt.close(fig)
    buf.seek(0)
    return buf
