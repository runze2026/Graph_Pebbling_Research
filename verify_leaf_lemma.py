"""Day 2: Verify Lemma 1 (Leaf Target Sufficiency).

Fast strategy using archived pebbling numbers:
  At S = pi(G), verify every configuration can pebble EVERY vertex (not just leaves).
  Combined with Day 1 result that S = pi(G)-1 fails for some leaf, this confirms
  pi(G) = max{pi(G, u_L), pi(G, u_R)}.
"""

from collections import deque
import itertools
import json
from pathlib import Path

from networkx.algorithms import isomorphism

from graphs import create_tadpole_3, graph_metadata


def is_reachable(G, config, target):
    if config[target] > 0:
        return True
    queue = deque([config])
    visited = {config}
    while queue:
        curr = queue.popleft()
        if curr[target] > 0:
            return True
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
    return False


def _automorphisms(G, fix_vertex=None):
    """Automorphisms of G; if fix_vertex is set, only those fixing that vertex."""
    GM = isomorphism.GraphMatcher(G, G)
    autos = list(GM.isomorphisms_iter())
    if fix_vertex is None:
        return autos
    return [m for m in autos if m[fix_vertex] == fix_vertex]


def iter_unique_configs(G, S, fix_vertex=None):
    """Enumerate S-pebble configs, quotiented by Aut(G) or Aut_G(fix_vertex)."""
    n = G.number_of_nodes()
    automorphisms = _automorphisms(G, fix_vertex)
    if not automorphisms:
        automorphisms = [{v: v for v in G.nodes()}]
    seen = set()
    for p in itertools.combinations_with_replacement(range(n), S):
        config = [0] * n
        for idx in p:
            config[idx] += 1
        config_t = tuple(config)
        if config_t in seen:
            continue
        for mapping in automorphisms:
            temp = [0] * n
            for u, v in mapping.items():
                temp[v] = config[u]
            seen.add(tuple(temp))
        yield config_t


def n_minus_one_bound_config(G, target):
    """One pebble on every vertex except target (|D| = n-1, no move possible)."""
    n = G.number_of_nodes()
    cfg = [0] * n
    for v in range(n):
        if v != target:
            cfg[v] = 1
    return tuple(cfg)


def assert_sanity_checks(G, s1, s2, per_target, vertex_by_name):
    """Universal n-1 lower bound; left-right symmetry when s1 == s2."""
    n = G.number_of_nodes()
    for name, pi_t in per_target.items():
        vtx = vertex_by_name[name]
        assert pi_t >= n, (
            f"T(3,{s1},{s2}): pi({name})={pi_t} violates n-1 lower bound (need >= {n})"
        )
        cfg = n_minus_one_bound_config(G, vtx)
        assert not is_reachable(G, cfg, vtx), (
            f"T(3,{s1},{s2}): n-1 bound config for {name} should be unsolvable"
        )
    if s1 == s2:
        assert per_target["a"] == per_target["b"], (
            f"T(3,{s1},{s2}): pi(a)={per_target['a']} != pi(b)={per_target['b']}"
        )
        assert per_target["u_L"] == per_target["u_R"], (
            f"T(3,{s1},{s2}): pi(u_L)={per_target['u_L']} != pi(u_R)={per_target['u_R']}"
        )


def verify_at_pi(s1, s2, pi_known):
    G = create_tadpole_3(s1, s2)
    meta = graph_metadata(G)
    n = G.number_of_nodes()
    targets = list(range(n))

    failures = {t: None for t in targets}
    checked = 0

    for config in iter_unique_configs(G, pi_known, fix_vertex=None):
        checked += 1
        for t in targets:
            if failures[t] is None and not is_reachable(G, config, t):
                failures[t] = config

    per_target_ok = {str(t): failures[t] is None for t in targets}
    all_vertices_ok = all(failures[t] is None for t in targets)

    return {
        "graph": f"T(3,{s1},{s2})",
        "s1": s1,
        "s2": s2,
        "diameter": meta["diameter"],
        "pi_known": pi_known,
        "configs_checked": checked,
        "u_L": meta["u_L"],
        "u_R": meta["u_R"],
        "all_vertices_reachable_at_pi": all_vertices_ok,
        "per_target_ok": per_target_ok,
        "first_failing_config": {
            str(t): list(failures[t]) if failures[t] else None for t in targets
        },
    }


def compute_per_target_pi_small(s1, s2, max_pi):
    """Full per-target pi for small graphs only (d <= 4)."""
    G = create_tadpole_3(s1, s2)
    meta = graph_metadata(G)
    d = meta["diameter"]
    n = meta["n_vertices"]
    start = n

    targets = [("c", 2), ("a", 0), ("b", 1), ("u_L", meta["u_L"])]
    if s1 != s2:
        targets.append(("u_R", meta["u_R"]))
    vertex_by_name = dict(targets)
    if s1 == s2:
        vertex_by_name["u_R"] = meta["u_R"]
    result = {}
    for name, vtx in targets:
        pi_t = None
        for S in range(start, max_pi + 1):
            ok = True
            for config in iter_unique_configs(G, S, fix_vertex=vtx):
                if not is_reachable(G, config, vtx):
                    ok = False
                    break
            if ok:
                pi_t = S
                break
        result[name] = pi_t

    if s1 == s2:
        result["u_R"] = result["u_L"]

    assert_sanity_checks(G, s1, s2, result, vertex_by_name)

    pi_leaves = max(result["u_L"], result["u_R"])
    return {
        "per_target": result,
        "pi_from_leaves": pi_leaves,
        "pi_from_all": max(result.values()),
        "lemma_holds": max(result.values()) == pi_leaves,
    }


def main():
    archived = [
        (1, 1, 9),
        (1, 2, 17),
        (2, 2, 33),
        (1, 3, 33),
    ]

    print("=" * 70, flush=True)
    print("Day 2 — Leaf Target Sufficiency Verification", flush=True)
    print("=" * 70, flush=True)

    results = []

    print("\n[1/2] Full per-target pi for d <= 4 ...", flush=True)
    for s1, s2, pi in archived:
        if s1 + s2 + 1 > 4:
            continue
        print(f"  T(3,{s1},{s2}) ...", flush=True)
        detail = compute_per_target_pi_small(s1, s2, pi)
        detail["graph"] = f"T(3,{s1},{s2})"
        detail["mode"] = "full_per_target"
        results.append(detail)
        pt = detail["per_target"]
        print(
            f"    pi(c)={pt['c']}, pi(a)={pt['a']}, pi(b)={pt['b']}, "
            f"pi(u_L)={pt['u_L']}, pi(u_R)={pt['u_R']}, "
            f"pi(G)={detail['pi_from_all']}, lemma={detail['lemma_holds']}",
            flush=True,
        )

    print("\n[2/2] All-vertex reachability at known pi(G) ...", flush=True)
    for s1, s2, pi in archived:
        if s1 + s2 + 1 <= 4:
            continue
        print(f"  T(3,{s1},{s2}) at S={pi} ...", flush=True)
        row = verify_at_pi(s1, s2, pi)
        row["mode"] = "all_vertices_at_pi"
        results.append(row)
        print(
            f"    checked {row['configs_checked']:,} configs, "
            f"all vertices OK: {row['all_vertices_reachable_at_pi']}",
            flush=True,
        )

    out = Path(__file__).parent / "data" / "leaf_lemma_verification.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nSaved: {out}", flush=True)

    ok = all(
        r.get("lemma_holds", r.get("all_vertices_reachable_at_pi"))
        for r in results
    )
    print("=" * 70, flush=True)
    print(f"Lemma verified for all archived instances: {ok}", flush=True)
    print("=" * 70, flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
