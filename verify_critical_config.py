"""Day 3: Verify critical configuration D* and build configs from graph metadata."""

import json
from pathlib import Path

from pebbling_solver import is_reachable
from graphs import create_tadpole_3, graph_metadata


def critical_config(G, target="u_R"):
    """Build D*: (2^d - 1) on leaf farthest from target, 1 on apex c."""
    meta = graph_metadata(G)
    d = meta["diameter"]
    n = meta["n_vertices"]
    cfg = [0] * n
    cfg[meta["c"]] = 1
    if target == "u_R":
        cfg[meta["u_L"]] = 2**d - 1
    elif target == "u_L":
        cfg[meta["u_R"]] = 2**d - 1
    else:
        raise ValueError("target must be 'u_L' or 'u_R'")
    return tuple(cfg)


def verify_instance(s1, s2):
    G = create_tadpole_3(s1, s2)
    meta = graph_metadata(G)
    d = meta["diameter"]
    for target_name, target_v in [("u_R", meta["u_R"]), ("u_L", meta["u_L"])]:
        cfg = critical_config(G, target=target_name)
        reachable = is_reachable(G, cfg, target_v)
        yield {
            "graph": f"T(3,{s1},{s2})",
            "diameter": d,
            "target": target_name,
            "target_vertex": target_v,
            "config": list(cfg),
            "total_pebbles": sum(cfg),
            "expected_total": 2**d,
            "reachable": reachable,
            "confirms_lower_bound": not reachable,
        }


def main():
    instances = [(1, 1), (1, 2), (2, 2), (1, 3)]
    results = list(
        row
        for s1, s2 in instances
        for row in verify_instance(s1, s2)
    )

    print("=" * 70)
    print("Day 3 — Critical Configuration Verification")
    print("=" * 70)
    for row in results:
        status = "FAILS (good)" if row["confirms_lower_bound"] else "REACHABLE (bad)"
        print(
            f"{row['graph']} target {row['target']} "
            f"S={row['total_pebbles']} -> {status}  config={tuple(row['config'])}"
        )

    ok = all(r["confirms_lower_bound"] for r in results)
    out = Path(__file__).parent / "data" / "critical_config_verification.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nSaved: {out}")
    print("=" * 70)
    print(f"All critical configs unsolvable: {ok}")
    print("=" * 70)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
