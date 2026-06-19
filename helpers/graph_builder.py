import random
import string
from typing import Literal, Optional, Tuple

import networkx as nx

from models.graph import GraphRequest


def generate_random_graph(
    vertex_count: int,
    directed: bool,
    graph_type: Literal["default", "dag", "scc", "properties"] = "default",
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
        k_max = max(2, min(4, vertex_count - 1))
        k = random.randint(2, k_max)
        indices = list(range(vertex_count))
        random.shuffle(indices)
        groups: list[list[int]] = [[indices.pop()] for _ in range(k)]
        for idx in indices:
            groups[random.randint(0, k - 1)].append(idx)

        if all(len(g) == 1 for g in groups) and len(groups) >= 2:
            groups[0].extend(groups.pop())

        for group in groups:
            if len(group) >= 2:
                cycle = group[:]
                random.shuffle(cycle)
                for gi in range(len(cycle)):
                    G.add_edge(cycle[gi], cycle[(gi + 1) % len(cycle)])

        for gi in range(k - 1):
            src = random.choice(groups[gi])
            tgt = random.choice(groups[gi + 1])
            G.add_edge(src, tgt)
            if random.random() < 0.3:
                src2 = random.choice(groups[gi])
                tgt2 = random.choice(groups[gi + 1])
                if not G.has_edge(src2, tgt2):
                    G.add_edge(src2, tgt2)
    elif graph_type == "properties":
        G = nx.DiGraph() if directed else nx.Graph()
        G.add_nodes_from(range(vertex_count))
        cycle = list(range(vertex_count))
        random.shuffle(cycle)
        for ci in range(vertex_count):
            G.add_edge(cycle[ci], cycle[(ci + 1) % vertex_count])
        p_extra = min(0.3, 3.0 / vertex_count)
        for i in range(vertex_count):
            for j in range(vertex_count):
                if i == j or G.has_edge(i, j):
                    continue
                # Undirected: only consider each pair once to avoid duplicate work.
                if not directed and j < i:
                    continue
                if random.random() < p_extra:
                    G.add_edge(i, j)
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
