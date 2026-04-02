import random
import string

import networkx as nx

from models.graph import GraphRequest


def generate_random_graph(vertex_count: int, directed: bool) -> nx.Graph:
    if vertex_count <= 26:
        labels = list(string.ascii_uppercase[:vertex_count])
    else:
        labels = [f"V{i}" for i in range(1, vertex_count + 1)]

    p_base = min(0.4, 4.0 / vertex_count)
    p = p_base / 2 if directed else p_base

    G = nx.gnp_random_graph(vertex_count, p, directed=directed, seed=random.randint(0, 2**31))

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
