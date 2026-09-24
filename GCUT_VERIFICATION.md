# GCUT_VERIFICATION: Transferability to General 2D Cutting-Stock Instances

## What this is

This applies this repository's MaxRects nesting algorithm
(`cutting_stock_optimizer/core.py`) to real, publicly available,
peer-reviewed benchmark instances from Beasley (1985), "Algorithms for
unconstrained two-dimensional guillotine cutting," *Journal of the
Operational Research Society* 36, 297-306, distributed as the "gcut"
series via ESICUP.

**Source data**: https://github.com/ESICUP/datasets (`2d_rectangular/gcut/`)

## Why this exists

Exhibit J-1's original demonstration used a representative apparel
cutting order, and its ESICUP extension used the Christofides &
Whitlock (1977) textile-cutting instances. Both are drawn from the
same general problem family, but both sit within the cutting-stock
literature's textile-adjacent tradition. This addition tests the same
algorithm against a different, separately published general 2D
cutting-stock benchmark with no connection to textiles specifically,
supporting the petition's claim that this methodology is transferable
to other cutting-intensive manufacturing sectors, such as sheet-metal
and leather goods, that face the same underlying mathematical problem.

## Results (reported exactly as obtained)

| Instance | Pieces | Naive baseline | MaxRects optimizer | Improvement |
|---|---|---|---|---|
| gcut1 | 10 | 43.6% | 65.4% | +21.8 points |
| gcut2 | 20 | 39.9% | 73.2% | +33.3 points |
| gcut3 | 30 | 46.6% | 81.5% | +34.9 points |
| gcut4 | 50 | 46.8% | 90.0% | +43.2 points |
| gcut5 | 10 | 43.6% | 72.7% | +29.1 points |

**Average improvement across all five instances: +32.5 percentage points.**

No instance was selected or excluded to favor a particular result.

## Running it yourself

```
python run_gcut_benchmark.py
```

Requires no dependencies beyond this repository's own package.
