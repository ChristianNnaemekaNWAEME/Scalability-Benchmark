"""
gcut_loader.py

Parser for the ESICUP "gcut" benchmark format (Beasley, 1985,
"Algorithms for unconstrained two-dimensional guillotine cutting,"
Journal of the Operational Research Society 36, 297-306), a classic,
peer-reviewed general 2D cutting-stock benchmark distinct from the
textile-specific cgcut instances already used in Exhibit J-1.

Source: https://github.com/ESICUP/datasets (2d_rectangular/gcut/)

Format (identical to cgcut):
    line 1: number of piece types (m)
    line 2: stock sheet width, height
    lines 3..m+2: piece width, height, value
"""

from cutting_stock_optimizer import Piece


def load_gcut_instance(path):
    with open(path) as f:
        lines = [line.split() for line in f.read().strip().split("\n")]

    m = int(lines[0][0])
    sheet_w, sheet_h = map(float, lines[1])

    pieces = []
    for i in range(2, 2 + m):
        width, height, value = lines[i]
        width, height = float(width), float(height)
        pieces.append(Piece(id=f"p{i-1}", width=width, height=height, allow_rotation=True))

    return sheet_w, sheet_h, pieces
