"""Day 4-5: Verify max pebbles on b reachable from critical configuration D*."""

from collections import deque
import json
from pathlib import Path

from graphs import create_tadpole_3, graph_metadata
from verify_critical_config import critical_config


def max_pebbles_at_vertex(G, start_config, vertex):
    """Maximum pebble count at `vertex` over all states reachable from start_config."""
    n = G.number_of_nodes()
    start = tuple(start_config)
    best = start[vertex]
    queue = deque([start])
    visited = {start}

    while queue:
        curr = queue.popleft()
        best = max(best, curr[vertex])
        for u in G.nodes():
            if curr[u] >= 2:
                for v in G.neighbors(u):
                    nxt = list(curr)
                    nxt[u] -= 2
                    nxt[v] += 1
                    nxt_t = tuple(nxt)
                    if nxt_t not in visited:
                        visited.add(nxt_t)
                        queue.append(nxt_t)

    return best, len(visited)


def verify_instance(s1, s2):
    G = create_tadpole_3(s1, s2)
    meta = graph_metadata(G)
    d = meta["diameter"]
    s2_len = meta["s2"]
    threshold = 2 ** s2_len
    formula_max_b = 2 ** s2_len - 1

    cfg = critical_config(G, target="u_R")
    max_b, states = max_pebbles_at_vertex(G, cfg, meta["b"])
    max_a, _ = max_pebbles_at_vertex(G, cfg, meta["a"])

    return {
        "graph": f"T(3,{s1},{s2})",
        "diameter": d,
        "s1": s1,
        "s2": s2_len,
        "threshold_on_b": threshold,
        "formula_max_b": formula_max_b,
        "max_pebbles_at_b": max_b,
        "max_pebbles_at_a": max_a,
        "reachable_states": states,
        "below_threshold": max_b < threshold,
    }


def main():
    instances = [(1, 1), (1, 2), (2, 2), (1, 3)]
    results = [verify_instance(s1, s2) for s1, s2 in instances]

    print("=" * 70)
    print("Day 4-5 — Max pebbles at b from critical configuration")
    print("=" * 70)
    for row in results:
        print(
            f"{row['graph']}: max p(b)={row['max_pebbles_at_b']}, "
            f"threshold=2^{{s2}}={row['threshold_on_b']}, "
            f"OK={row['below_threshold']}"
        )

    out = Path(__file__).parent / "data" / "b_capacity_verification.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nSaved: {out}")
    ok = all(r["below_threshold"] for r in results)
    print("=" * 70)
    print(f"All instances satisfy max p(b) < 2^s2: {ok}")
    print("=" * 70)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
