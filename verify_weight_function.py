"""Day 8+: Verify path-spine + apex weight function for T(3,s1,s2)."""

import itertools
import json
from pathlib import Path

from networkx.algorithms import isomorphism

from graphs import create_tadpole_3, graph_metadata
from pebbling_solver import is_reachable
from search_weight_function import build_weights_path_spine_plus_apex, test_validity


def main():
    import sys

    quick = "--quick" in sys.argv
    instances = [(1, 1)] if quick else [(1, 1), (1, 2), (2, 1), (2, 2)]
    results = []

    print("=" * 70)
    print("Day 8 — Path-Spine Weight Function Verification")
    print("=" * 70)

    for s1, s2 in instances:
        G = create_tadpole_3(s1, s2)
        meta = graph_metadata(G)
        d = meta["diameter"]
        expected = 2**d + 1

        for target_name, target in [("u_R", meta["u_R"]), ("u_L", meta["u_L"])]:
            weights = build_weights_path_spine_plus_apex(G, target)
            row = test_validity(G, weights, target)
            valid, viols, checked, w1 = row
            pred = int(w1) + 1
            status = "VALID" if valid else "INVALID"
            print(
                f"T(3,{s1},{s2}) target={target_name}: w(1_G)={w1:.0f}, "
                f"pred_pi<={pred}, expected={expected}, {status}, checked={checked}"
            )
            if viols:
                print(f"  violation: {viols[0]}")
            results.append(
                {
                    "graph": f"T(3,{s1},{s2})",
                    "target": target_name,
                    "builder": "path_spine_plus_apex",
                    "w_unit": w1,
                    "predicted": pred,
                    "expected_pi": expected,
                    "valid": valid,
                    "configs_checked": checked,
                    "violations": viols,
                    "weights": {str(k): v for k, v in weights.items()},
                }
            )

    # d=5 normalization check only (full enumeration deferred)
    for s1, s2 in [(2, 2), (1, 3)]:
        G = create_tadpole_3(s1, s2)
        meta = graph_metadata(G)
        d = meta["diameter"]
        w = build_weights_path_spine_plus_apex(G, meta["u_R"])
        w1 = sum(w.values())
        results.append(
            {
                "graph": f"T(3,{s1},{s2})",
                "target": "u_R",
                "builder": "path_spine_plus_apex",
                "w_unit": w1,
                "predicted": int(w1) + 1,
                "expected_pi": 2**d + 1,
                "valid": None,
                "note": "normalization only; full validity check deferred (d=5)",
                "weights": {str(k): v for k, v in w.items()},
            }
        )
        print(
            f"T(3,{s1},{s2}) target=u_R: w(1_G)={w1:.0f} "
            f"(normalization check, d=5 full enum deferred)"
        )

    out = Path(__file__).parent / "data" / "weight_function_day8.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nSaved: {out}")
    if not quick:
        print("(Use --quick for T(3,1,1) only; full d=4 results in data/weight_function_day8.json)")
    print("=" * 70)


if __name__ == "__main__":
    main()
