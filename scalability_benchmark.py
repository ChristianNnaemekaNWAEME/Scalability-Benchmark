"""
scalability_benchmark.py

Exhibit J-8: Computational scalability of this repository's MaxRects
nesting algorithm at industrial problem sizes.

Current (2026) published research in this field treats computational
efficiency at scale as a central, active concern: for example, Abdou,
K. et al., "Nest smarter, not harder: a hybrid vision-based deep
reinforcement learning agent for packing 2D irregular geometries by
rotational placement," Journal of Intelligent Manufacturing 37,
1753-1767 (2026), frames its own contribution partly around a "97%
improvement in computation time" over existing nesting software on
sheet-metal industry data. That paper's method and code are not
publicly available, so it cannot be reproduced or directly benchmarked
against here. This experiment instead independently measures this
repository's own algorithm against the same general concern,
computational practicality as problem size grows, using randomly
generated instances at problem sizes spanning realistic production
runs, from small batches to large industrial cutting orders.

Results are reported exactly as obtained.
"""

import sys
import os
import time
sys.path.insert(0, os.path.dirname(__file__))

import random
from cutting_stock_optimizer import CuttingStockOptimizer, ShelfPacker, Piece


def generate_random_pieces(n, seed, min_size=5, max_size=40):
    rng = random.Random(seed)
    return [
        Piece(id=f"p{i}", width=rng.randint(min_size, max_size),
              height=rng.randint(min_size, max_size), allow_rotation=True)
        for i in range(n)
    ]


def run_at_scale(n_pieces, sheet_w=100, sheet_h=100, seed=42):
    pieces = generate_random_pieces(n_pieces, seed, min_size=5, max_size=sheet_w // 3)
    total_area = sum(p.area for p in pieces)

    start = time.perf_counter()
    optimizer = CuttingStockOptimizer(sheet_w, sheet_h)
    optimizer.pack(pieces)
    elapsed = time.perf_counter() - start

    sheets_used = len(optimizer.sheets)
    utilization = total_area / (sheets_used * sheet_w * sheet_h)

    return elapsed, sheets_used, utilization


def main():
    problem_sizes = [50, 100, 250, 500, 1000, 2000]
    print(f"{'Pieces':>8} {'Runtime (s)':>13} {'Sheets Used':>13} {'Utilization':>13}")
    results = []
    for n in problem_sizes:
        elapsed, sheets, util = run_at_scale(n)
        print(f"{n:>8} {elapsed:>13.3f} {sheets:>13} {util*100:>12.1f}%")
        results.append((n, elapsed, sheets, util))

    print("\nResults reported exactly as obtained, not adjusted or selected")
    print("to favor any particular outcome. Randomly generated instances,")
    print("fixed seed for reproducibility.")

    import csv
    with open("scalability_results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["n_pieces", "runtime_seconds", "sheets_used", "utilization"])
        writer.writerows(results)


if __name__ == "__main__":
    main()
