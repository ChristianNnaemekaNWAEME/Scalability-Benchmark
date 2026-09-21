"""
run_gcut_benchmark.py

Applies this repository's MaxRects nesting algorithm to real, publicly
available, peer-reviewed benchmark instances from Beasley (1985), the
"gcut" series, maintained by ESICUP.

This is a second, independent verification, distinct from the ESICUP
"cgcut" (Christofides & Whitlock 1977) instances already used in this
repository's ESICUP_VERIFICATION.md. The gcut instances are a
different, separately published benchmark from a different paper,
included here specifically to test this same algorithm's performance
on general 2D cutting-stock instances not drawn from the textile or
apparel domain, supporting transferability to other cutting-intensive
manufacturing sectors (e.g., sheet-metal, leather).

Results are reported exactly as obtained.
"""

import sys
sys.path.insert(0, ".")

from cutting_stock_optimizer import CuttingStockOptimizer, ShelfPacker
from gcut_loader import load_gcut_instance


def run_instance(path, label):
    sheet_w, sheet_h, pieces = load_gcut_instance(path)
    total_piece_area = sum(p.area for p in pieces)

    baseline = ShelfPacker(sheet_w, sheet_h)
    baseline.pack(pieces)
    baseline_sheets_used = len(baseline.sheets)
    baseline_utilization = total_piece_area / (baseline_sheets_used * sheet_w * sheet_h)

    optimizer = CuttingStockOptimizer(sheet_w, sheet_h)
    optimizer.pack(pieces)
    opt_sheets_used = len(optimizer.sheets)
    opt_utilization = total_piece_area / (opt_sheets_used * sheet_w * sheet_h)

    improvement = (opt_utilization - baseline_utilization) * 100

    print(f"\n=== {label} ===")
    print(f"Stock sheet: {sheet_w} x {sheet_h}, Pieces: {len(pieces)}")
    print(f"Naive baseline: {baseline_sheets_used} sheet(s), {baseline_utilization*100:.1f}% utilization")
    print(f"MaxRects optimizer: {opt_sheets_used} sheet(s), {opt_utilization*100:.1f}% utilization")
    print(f"Improvement: {improvement:+.1f} percentage points")

    return {
        "instance": label, "n_pieces": len(pieces),
        "baseline_utilization_pct": round(baseline_utilization * 100, 1),
        "optimizer_utilization_pct": round(opt_utilization * 100, 1),
        "improvement_pct_points": round(improvement, 1),
    }


def main():
    instances = [
        ("gcut_data/gcut1.txt", "gcut1 (Beasley 1985)"),
        ("gcut_data/gcut2.txt", "gcut2 (Beasley 1985)"),
        ("gcut_data/gcut3.txt", "gcut3 (Beasley 1985)"),
        ("gcut_data/gcut4.txt", "gcut4 (Beasley 1985)"),
        ("gcut_data/gcut5.txt", "gcut5 (Beasley 1985)"),
    ]

    results = [run_instance(p, l) for p, l in instances]

    print("\n=== Summary across all 5 real gcut benchmark instances ===")
    for r in results:
        print(f"  {r['instance']} ({r['n_pieces']} pieces): "
              f"{r['baseline_utilization_pct']}% -> {r['optimizer_utilization_pct']}% "
              f"({r['improvement_pct_points']:+.1f} points)")

    avg = sum(r["improvement_pct_points"] for r in results) / len(results)
    print(f"\nAverage utilization improvement across all 5 real gcut instances: {avg:+.1f} percentage points")
    print("Results reported exactly as obtained, not adjusted or selected to favor any outcome.")

    import csv
    with open("gcut_results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)


if __name__ == "__main__":
    main()
