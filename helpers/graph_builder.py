import random
import string
from typing import Literal, Optional, Tuple

import networkx as nx

from models.graph import GraphRequest


def generate_random_graph(
    vertex_count: int,
    directed: bool,
    graph_type: Literal["default", "dag", "scc"] = "default",
    include_weights: bool = False,
    weight_range: Tuple[float, float] = (0.1, 2.0),
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
        # Ensure DAG is weakly connected
        undirected_view = G.to_undirected()
        components = list(nx.connected_components(undirected_view))
        for ci in range(len(components) - 1):
            # Get a node from each component and add edge in topological order
            nodes_a = sorted(components[ci])
            nodes_b = sorted(components[ci + 1])
            # Add edge from higher-indexed component to lower to maintain DAG property
            G.add_edge(nodes_a[-1], nodes_b[0])
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
        # Ensure graph is connected
        if directed:
            # For directed graphs, ensure weak connectivity
            undirected_view = G.to_undirected()
            components = list(nx.connected_components(undirected_view))
            for i in range(len(components) - 1):
                node_a = next(iter(components[i]))
                node_b = next(iter(components[i + 1]))
                G.add_edge(node_a, node_b)
        else:
            # For undirected graphs, connect all components
            components = list(nx.connected_components(G))
            for i in range(len(components) - 1):
                node_a = next(iter(components[i]))
                node_b = next(iter(components[i + 1]))
                G.add_edge(node_a, node_b)

    mapping = {i: labels[i] for i in range(vertex_count)}
    G = nx.relabel_nodes(G, mapping)

    # Assign random weights if requested
    if include_weights:
        for u, v in G.edges():
            G[u][v]["weight"] = round(random.uniform(*weight_range), 2)

    return G


def build_graph(req: GraphRequest) -> nx.Graph:
    G = nx.DiGraph() if req.directed else nx.Graph()
    if req.nodes:
        G.add_nodes_from(req.nodes)
    for e in req.edges:
        if e.weight is not None:
            G.add_edge(e.source, e.target, weight=e.weight)
        else:
            G.add_edge(e.source, e.target)
    return G


def build_directed_graph(req: GraphRequest) -> nx.DiGraph:
    G: nx.DiGraph = nx.DiGraph()
    if req.nodes:
        G.add_nodes_from(req.nodes)
    for e in req.edges:
        if e.weight is not None:
            G.add_edge(e.source, e.target, weight=e.weight)
        else:
            G.add_edge(e.source, e.target)
    return G
