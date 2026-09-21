# Cutting Stock Optimizer

A 2D rectangle-nesting engine for the **Cutting Stock Problem (CSP)** — the
NP-hard combinatorial optimization problem of arranging a set of rectangular
pieces onto fixed-size stock sheets (fabric rolls, leather hides, sheet metal)
while minimizing trim loss.

This is an independent, open-source implementation I built to continue
developing the digitization-and-optimization work described in my professional
background, applying the **MaxRects "Best Area Fit" algorithm** (Jylänki,
2010) — a well-established nesting heuristic — from scratch in Python, with a
naive baseline packer included for direct before/after comparison.

## Why this exists

The Cutting Stock Problem recurs across textile, leather, and sheet-metal
manufacturing: whatever the material, the underlying question is the same —
how do you lay out a set of parts on a sheet to waste as little material as
possible? This project is a from-scratch, material-agnostic implementation of
that optimization step, independent of any proprietary tooling, intended to
demonstrate the algorithmic side of that pipeline (digitized pattern data →
optimized nesting → cut layout) in a form that's inspectable, testable, and
extensible.

## What's included

- **`core.py`** — the MaxRects packer: places pieces using a best-area-fit
  heuristic, splits and prunes the free-rectangle list as pieces are placed,
  supports rotation, and spills onto additional sheets when needed.
- **`baseline.py`** — a deliberately naive "shelf" packer (left-to-right,
  row by row, no optimization), used as the "before" comparison point.
- **`visualize.py`** — renders packed sheets as labeled matplotlib layout
  diagrams.
- **`tests/`** — correctness tests verifying no two placed pieces ever
  overlap, every piece stays within sheet bounds, and every input piece is
  placed exactly once.
- **`examples/garment_cutting_demo.py`** — a realistic demo: a small batch
  cutting order (front/back panels, sleeves, collars, cuffs, pockets) is
  packed both ways and the results are compared.

## Results (from the included demo)

Running `examples/garment_cutting_demo.py` on a 64-piece cutting order
(8 garments × 8 pattern pieces each) onto 160×200 stock sheets:

| | Naive (shelf) layout | MaxRects-optimized layout |
|---|---|---|
| Sheets required | 6 | 4 |
| Material utilization | 47.4% | 71.1% |
| **Waste** | **52.6%** | **28.9%** |

That's a **23.7 percentage-point reduction in waste** and **2 fewer stock
sheets** for the same cutting order, from the nesting algorithm alone, with no
change to the pieces themselves.

**Naive layout:**
![Naive layout](examples/output/naive_layout.png)

**Optimized layout:**
![Optimized layout](examples/output/optimized_layout.png)

*(These specific figures are from the included synthetic demo order, not from
proprietary production data. Results on any real cutting order will depend on
the actual size and shape distribution of the pieces involved.)*

## Installation

```bash
git clone https://github.com/ChristianNwaeme/cutting-stock-optimizer.git
cd cutting-stock-optimizer
pip install -r requirements.txt
```

## Usage

```python
from cutting_stock_optimizer import Piece, CuttingStockOptimizer

pieces = [
    Piece(id="panel_1", width=55, height=70),
    Piece(id="sleeve_1", width=25, height=60),
    Piece(id="collar_1", width=40, height=10),
    # ...
]

optimizer = CuttingStockOptimizer(sheet_width=160, sheet_height=200)
placements = optimizer.pack(pieces)

print(optimizer.summary())
# {'num_sheets': ..., 'waste_percent': ..., 'utilization_percent': ..., ...}
```

Run the full demo (prints stats and saves comparison figures to
`examples/output/`):

```bash
python examples/garment_cutting_demo.py
```

Run the test suite:

```bash
python tests/test_core.py
```

## Algorithm notes

MaxRects tracks the set of maximal free rectangles remaining on each sheet.
For each incoming piece (processed largest-area-first), it evaluates every
free rectangle the piece could fit into — in either orientation, if rotation
is allowed — and selects the placement that leaves the least leftover area
(*Best Area Fit*), breaking ties by the shorter leftover side. After
placement, the free-rectangle list is split around the newly placed piece and
pruned of any free rectangle now fully contained within another, keeping the
free-space representation compact. This is a well-documented, practical
heuristic for 2D nesting problems of this kind, distinct from — and
complementary to — the marker-generation functionality already offered by
commercial CAD/nesting packages, since the focus here is the underlying
optimization primitive itself.

## Roadmap

- [ ] Column-generation-based exact/near-exact solver for smaller problem
      instances, for comparison against the MaxRects heuristic
- [ ] Support for irregular (non-rectangular) piece outlines
- [ ] DXF import, to connect directly to digitized pattern data
- [ ] Benchmark against standard CSP test datasets from the OR literature

## License

MIT — see [LICENSE](LICENSE).
