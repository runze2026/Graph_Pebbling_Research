# Graph Pebbling Research — Double-Tailed Tadpole Graphs

Exact pebbling numbers of the family $T(3,s_1,s_2)$.

## Project Structure

```
Graph_Pebbling_Research/
├── pebbling_solver.py          # Exhaustive pebbling number solver
├── graphs.py                   # Graph constructors & vertex labeling
├── data/
│   └── computational_results.json
├── docs/
│   └── day1_checklist.md
└── paper/
    ├── main.tex
    └── sections/
        ├── 01_preliminaries.tex
        └── 05_computational_results.tex
```

## Vertex Convention

| Symbol | Role |
|--------|------|
| 0 (a) | Triangle vertex, root of left tail |
| 1 (b) | Triangle vertex, root of right tail |
| 2 (c) | Triangle apex (no tail attached) |
| u_L | Left leaf |
| u_R | Right leaf |

## Verified Results

| Graph | diam | π(G) |
|-------|-----:|-----:|
| T(3,1,1) | 3 | 9 |
| T(3,1,2) | 4 | 17 |
| T(3,2,2) | 5 | 33 |
| T(3,1,3) | 5 | 33 |

**Conjecture:** $\pi(T(3,s_1,s_2)) = 2^{s_1+s_2+1}+1$.

## Run Solver

```bash
python pebbling_solver.py          # Day 1 summary
python verify_leaf_lemma.py        # Day 2 lemma verification
python verify_critical_config.py   # Day 3 critical configuration
python verify_b_capacity.py        # Day 4-5 max p(b) check
python verify_weight_function.py   # Day 6-7 weight experiments
```

## Build Paper

```bash
cd paper && pdflatex main.tex
```
