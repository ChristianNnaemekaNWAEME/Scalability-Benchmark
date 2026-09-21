# Exhibit J-8: Computational Scalability at Industrial Problem Sizes

## What this is

This measures the runtime and material-utilization performance of
this repository's MaxRects nesting algorithm as problem size scales
from small batches (50 pieces) to large industrial cutting orders
(2,000 pieces), using randomly generated rectangular instances with a
fixed random seed for reproducibility.

## Why this exists

Current (2026) published research in this field treats computational
efficiency at industrial scale as a central, active concern. For
example, Abdou, K., Ibrahim, A. F., Binder, K., & Huber, M. F.,
"Nest smarter, not harder: a hybrid vision-based deep reinforcement
learning agent for packing 2D irregular geometries by rotational
placement," *Journal of Intelligent Manufacturing* 37, 1753-1767
(2026), frames its own contribution partly around a "97% improvement
in computation time" over existing nesting software on sheet-metal
industry data.

That paper's method and code are not publicly released, so it cannot
be reproduced or directly benchmarked against here, and no claim of
comparison to it is made. This experiment instead independently
measures this repository's own algorithm against the same underlying
concern the current literature raises, whether a nesting method
remains computationally practical as problem size grows to realistic
industrial scale, using this repository's own code.

## Results (reported exactly as obtained)

| Pieces | Runtime (seconds) | Sheets Used | Utilization |
|---|---|---|---|
| 50 | 0.001 | 2 | 80.9% |
| 100 | 0.003 | 4 | 86.7% |
| 250 | 0.008 | 9 | 95.8% |
| 500 | 0.018 | 20 | 91.2% |
| 1,000 | 0.040 | 38 | 96.8% |
| 2,000 | 0.104 | 76 | 96.3% |

Runtime grows sub-quadratically across a 40-fold increase in problem
size (roughly 100x runtime increase for a 40x size increase), and
material utilization remains high (generally above 90%) even at the
largest tested scale. No instance size was selected or excluded to
favor a particular outcome; minor run-to-run variation in the
reported runtimes is expected wall-clock measurement noise, not a
change in algorithm output (sheets used and utilization are
deterministic and reproduce exactly).

## Running it yourself

```
python scalability_benchmark.py
```

Requires no dependencies beyond this repository's own package and the
Python standard library.
