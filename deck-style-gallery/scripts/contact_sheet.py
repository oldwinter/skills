#!/usr/bin/env python3
"""Tile slide PNGs into one 2-column contact sheet for side-by-side review.

    python3 contact_sheet.py sheet.png a.png b.png c.png d.png
"""
import sys

from PIL import Image

W, H, GAP = 1600, 900, 20


def main() -> None:
    out, imgs = sys.argv[1], sys.argv[2:]
    rows = (len(imgs) + 1) // 2
    sheet = Image.new("RGB", (W * 2 + GAP, rows * H + (rows - 1) * GAP), "#888")
    for i, path in enumerate(imgs):
        tile = Image.open(path).convert("RGB").resize((W, H), Image.LANCZOS)
        sheet.paste(tile, ((i % 2) * (W + GAP), (i // 2) * (H + GAP)))
    sheet.save(out)
    print(out)


if __name__ == "__main__":
    main()
