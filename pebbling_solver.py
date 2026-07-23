from collections import deque
import itertools
import math
import time
from networkx.algorithms import isomorphism

from graphs import (
    create_tadpole_3_1_1,
    create_tadpole_3_1_2,
    create_tadpole_3_1_3,
    create_tadpole_3_2_2,
    create_tadpole_3_2_3,
    graph_metadata,
)

def is_reachable(G, config, target):
    if config[target] > 0:
        return True
    queue = deque([config])
    visited = {config}
    while queue:
        curr_state = queue.popleft()
        if curr_state[target] > 0:
            return True
        for u in G.nodes():
            if curr_state[u] >= 2:
                for v in G.neighbors(u):
                    next_state = list(curr_state)
                    next_state[u] -= 2
                    next_state[v] += 1
                    next_state_t = tuple(next_state)
                    if next_state_t not in visited:
                        visited.add(next_state_t)
                        queue.append(next_state_t)
    return False

def solve_with_target_pruning_stream(G, graph_name, start_S):
    """
    流式学术求解器：优化内存占用与同构去重，提供实时进度反馈
    """
    print(f"\n🚀 [Solver] Starting targeted search for {graph_name}...")
    start_time = time.time()
    
    # 提取所有叶子节点
    leaves = [v for v, d in G.degree() if d == 1]
    print(f"  -> Leaf nodes detected (Target Set): {leaves}")
    
    num_nodes = G.number_of_nodes()
    
    # 获取自同构群
    GM = isomorphism.GraphMatcher(G, G)
    automorphisms = list(GM.isomorphisms_iter())
    
    for S in range(start_S, 100):
        print(f"\n  Testing S = {S} ...")
        
        total_to_generate = math.comb(S + num_nodes - 1, num_nodes - 1)
        print(f"  -> Raw combinations to generate: {total_to_generate:,}")
        
        seen_isomorphs = set()
        checked_count = 0
        unique_count = 0
        all_passed = True
        bad_config = None
        bad_target = None
        
        last_report_time = time.time()
        
        # 流式生成组合，边生成边检查，避免一次性载入内存
        for p in itertools.combinations_with_replacement(range(num_nodes), S):
            checked_count += 1
            
            # 1. 快速构建配置
            config = [0] * num_nodes
            for idx in p:
                config[idx] += 1
            config_t = tuple(config)
            
            # 2. 同构去重检查
            if config_t in seen_isomorphs:
                continue
                
            # 标记同构
            for mapping in automorphisms:
                temp = [0] * num_nodes
                for u, v in mapping.items():
                    temp[v] = config[u]
                seen_isomorphs.add(tuple(temp))
            
            unique_count += 1
            
            # 3. 实时可达性判定
            for target in leaves:
                if not is_reachable(G, config_t, target):
                    all_passed = False
                    bad_config = config_t
                    bad_target = target
                    break
            
            # 4. 进度条反馈（每过 5 秒或者每 10 万个配置打印一次进度）
            if checked_count % 100000 == 0 or (time.time() - last_report_time) > 5.0:
                percent = (checked_count / total_to_generate) * 100
                print(f"    Progress: {percent:.2f}% | Generated: {checked_count:,} | Unique Checked: {unique_count:,} ...", end="\r")
                last_report_time = time.time()
                
            if not all_passed:
                break
                
        # 换行清除进度条残余字符
        print()
        
        if all_passed:
            elapsed = time.time() - start_time
            print(f"  🎉 SUCCESS for {graph_name}!")
            print(f"  -> Pebbling Number pi(G) = {S}")
            print(f"  -> Computational Time: {elapsed:.2f} seconds\n")
            return S
        else:
            print(f"    [Worst-case at S={S}]: Config {bad_config} fails to reach leaf {bad_target}")

# Verified instances archived on Day 1 (see data/computational_results.json)
VERIFIED_INSTANCES = [
    (create_tadpole_3_1_1, "T(3, 1, 1)", 3, 9),
    (create_tadpole_3_1_2, "T(3, 1, 2)", 4, 17),
    (create_tadpole_3_2_2, "T(3, 2, 2)", 5, 33),
    (create_tadpole_3_1_3, "T(3, 1, 3)", 5, 33),
]


def print_day1_summary():
    """Print archived Day 1 results without re-running expensive searches."""
    print("=" * 60)
    print("Day 1 Archive — Verified Pebbling Numbers")
    print("=" * 60)
    print(f"{'Graph':<12} {'d':>3} {'pi(G)':>6} {'2^d+1':>6} {'u_L':>4} {'u_R':>4}")
    print("-" * 60)
    for factory, name, d, pi in VERIFIED_INSTANCES:
        meta = graph_metadata(factory())
        print(
            f"{name:<12} {d:>3} {pi:>6} {2**d + 1:>6} "
            f"{meta['u_L']:>4} {meta['u_R']:>4}"
        )
    print("-" * 60)
    print("Conjecture: pi(T(3,s1,s2)) = 2^(s1+s2+1) + 1")
    print("T(3,2,3) deferred — see docs/day1_checklist.md")
    print("=" * 60)


if __name__ == "__main__":
    print_day1_summary()
