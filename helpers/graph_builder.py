import random
import string
from typing import Literal

import networkx as nx

from models.graph import GraphRequest


def generate_random_graph(
    vertex_count: int,
    directed: bool,
    graph_type: Literal["default", "dag", "scc"] = "default",
) -> nx.Graph:
    if vertex_count <= 26:
        labels = list(string.ascii_uppercase[:vertex_count])
    else:
        labels = [f"V{i}" for i in range(1, vertex_count + 1)]

    rng = random.randint(0, 2**31)

    if graph_type == "dag":
        G: nx.Graph = nx.DiGraph()
        G.add_nodes_from(range(vertex_count))
        p = min(0.5, 3.0 / vertex_count)
        for i in range(vertex_count):
            for j in range(i + 1, vertex_count):
                if random.random() < p:
                    G.add_edge(i, j)
        if G.number_of_edges() == 0:
            for i in range(vertex_count - 1):
                G.add_edge(i, i + 1)
    elif graph_type == "scc":
        G = nx.DiGraph()
        G.add_nodes_from(range(vertex_count))
        k = max(2, min(4, vertex_count // 3))
        groups: list[list[int]] = [[] for _ in range(k)]
        for idx in range(vertex_count):
            groups[idx % k].append(idx)
        # make each group a directed cycle (strongly connected)
        for group in groups:
            if len(group) == 1:
                # single-node SCC — no self-loop needed
                pass
            else:
                for gi in range(len(group)):
                    G.add_edge(group[gi], group[(gi + 1) % len(group)])
        # add one forward cross-edge per consecutive group pair
        for gi in range(k - 1):
            G.add_edge(groups[gi][0], groups[gi + 1][0])
    else:
        p_base = min(0.4, 4.0 / vertex_count)
        p = p_base / 2 if directed else p_base
        G = nx.gnp_random_graph(vertex_count, p, directed=directed, seed=rng)
        if G.number_of_edges() == 0:
            for i in range(vertex_count - 1):
                G.add_edge(i, i + 1)

    mapping = {i: labels[i] for i in range(vertex_count)}
    return nx.relabel_nodes(G, mapping)


def build_graph(req: GraphRequest) -> nx.Graph:
    G = nx.DiGraph() if req.directed else nx.Graph()
    if req.nodes:
        G.add_nodes_from(req.nodes)
    for e in req.edges:
        G.add_edge(e.source, e.target)
    return G


def build_directed_graph(req: GraphRequest) -> nx.DiGraph:
    G: nx.DiGraph = nx.DiGraph()
    if req.nodes:
        G.add_nodes_from(req.nodes)
    for e in req.edges:
        G.add_edge(e.source, e.target)
    return G
