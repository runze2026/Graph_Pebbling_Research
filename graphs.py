"""Graph constructors for double-tailed tadpole graphs T(3, s1, s2).

Vertex convention (consistent across all instances):
    0 = a   (triangle vertex, root of left tail)
    1 = b   (triangle vertex, root of right tail)
    2 = c   (triangle apex; not incident to any tail)
    Left tail:  3, 4, ... attached to 0; leaf u_L has index 2 + s1
    Right tail: next indices attached to 1; leaf u_R is the last vertex

For T(3, s1, s2): n = 3 + s1 + s2 vertices, diam = s1 + s2 + 1.
"""

import networkx as nx


def create_tadpole_3(s1, s2):
    """General constructor for T(3, s1, s2)."""
    if s1 < 1 or s2 < 1:
        raise ValueError("s1 and s2 must be at least 1")
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2), (2, 0)])
    left = [3]
    G.add_edge(0, 3)
    for i in range(4, 3 + s1):
        G.add_edge(i - 1, i)
        left.append(i)
    right_start = 3 + s1
    G.add_edge(1, right_start)
    right = [right_start]
    for i in range(right_start + 1, 3 + s1 + s2):
        G.add_edge(i - 1, i)
        right.append(i)
    G.graph["s1"] = s1
    G.graph["s2"] = s2
    G.graph["u_L"] = left[-1]
    G.graph["u_R"] = right[-1]
    G.graph["apex"] = 2
    return G


def create_tadpole_3_1_1():
    """T(3,1,1): 5 vertices, diam=3, leaves 3 and 4."""
    return create_tadpole_3(1, 1)


def create_tadpole_3_1_2():
    """T(3,1,2): 6 vertices, diam=4, leaves 3 and 5."""
    return create_tadpole_3(1, 2)


def create_tadpole_3_2_2():
    """T(3,2,2): 7 vertices, diam=5, leaves 4 and 6."""
    return create_tadpole_3(2, 2)


def create_tadpole_3_1_3():
    """T(3,1,3): 7 vertices, diam=5, leaves 3 and 6."""
    return create_tadpole_3(1, 3)


def create_tadpole_3_2_3():
    """T(3,2,3): 8 vertices, diam=6, leaves 4 and 7 (deferred computation)."""
    return create_tadpole_3(2, 3)


def graph_metadata(G):
    """Return labeling metadata for documentation."""
    s1 = G.graph.get("s1")
    s2 = G.graph.get("s2")
    if s1 is None:
        raise ValueError("Graph missing s1/s2 metadata; use create_tadpole_3(s1, s2)")
    leaves = [v for v, d in G.degree() if d == 1]
    return {
        "n_vertices": G.number_of_nodes(),
        "diameter": s1 + s2 + 1,
        "s1": s1,
        "s2": s2,
        "a": 0,
        "b": 1,
        "c": 2,
        "u_L": G.graph["u_L"],
        "u_R": G.graph["u_R"],
        "leaves": sorted(leaves),
    }
