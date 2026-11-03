#!/usr/bin/env python3
"""Wrap rendered slide PNGs into a 16:9 PPTX, one full-bleed image per slide.
Text is not editable in the result: edit the HTML, re-render, rebuild.

    python3 build_pptx.py deck.pptx slide-1.png slide-2.png ...
"""
import sys

from pptx import Presentation
from pptx.util import Inches


def main() -> None:
    out, slides = sys.argv[1], sys.argv[2:]
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    for png in slides:
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        slide.shapes.add_picture(png, 0, 0, prs.slide_width, prs.slide_height)
    prs.save(out)
    print(out, len(slides), "slides")


if __name__ == "__main__":
    main()
