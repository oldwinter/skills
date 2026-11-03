#!/usr/bin/env python3
"""Download the Latin web fonts each slide pulls from Google Fonts into ./fonts
and rewrite the <link> tags to the local copy, so renders stop depending on the
network. CJK families (names containing SC/TC/JP/KR) stay on Google Fonts:
their subsets are large and a failure falls back to a local Noto CJK face that
looks the same.

    python3 vendor_fonts.py slide-1.html slide-2.html ...   (run in the slides dir)
"""
import hashlib
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/130 Safari/537.36"}
TAG = re.compile(r'<link\b[^>]*href="(https://fonts\.googleapis\.com/css2\?[^"]+)"[^>]*>')
CJK = re.compile(r"\b(SC|TC|JP|KR)\b")
FONTS = Path("fonts")


def fetch(url: str) -> bytes:
    err = None
    for _ in range(5):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()
        except OSError as e:
            err = e
    raise SystemExit(f"download failed: {url}: {err}")


def css_url(families: list[str]) -> str:
    q = "&".join("family=" + urllib.parse.quote(f.replace(" ", "+"), safe=":,;@.+") for f in families)
    return f"https://fonts.googleapis.com/css2?{q}&display=swap"


def vendor(families: list[str]) -> str:
    url = css_url(families)
    name = "g-" + hashlib.sha1(url.encode()).hexdigest()[:10] + ".css"
    if not (FONTS / name).exists():
        css = fetch(url).decode()
        keep = []
        for subset, block in re.findall(r"/\* ([\w-]+) \*/\s*(@font-face \{.*?\})", css, re.S):
            if subset not in ("latin", "latin-ext"):
                continue
            src = re.search(r"url\((https://[^)]+)\)", block).group(1)
            woff = "g-" + hashlib.sha1(src.encode()).hexdigest()[:12] + ".woff2"
            if not (FONTS / woff).exists():
                (FONTS / woff).write_bytes(fetch(src))
            keep.append(block.replace(src, woff).replace("font-display: swap", "font-display: block"))
        (FONTS / name).write_text("\n".join(keep))
    return f"fonts/{name}"


def main() -> None:
    FONTS.mkdir(exist_ok=True)
    for html in map(Path, sys.argv[1:]):
        text = html.read_text()

        def swap(m: re.Match) -> str:
            query = urllib.parse.urlsplit(m.group(1).replace("&amp;", "&")).query
            fams = [v for k, v in urllib.parse.parse_qsl(query) if k == "family"]
            latin = [f for f in fams if not CJK.search(f)]
            cjk = [f for f in fams if CJK.search(f)]
            tags = [f'<link rel="stylesheet" href="{vendor(latin)}">'] if latin else []
            if cjk:
                tags.append(f'<link rel="stylesheet" href="{css_url(cjk).replace("&", "&amp;")}">')
            return "".join(tags)

        new = TAG.sub(swap, text)
        if new != text:
            html.write_text(new)
            print(f"{html}: vendored")


if __name__ == "__main__":
    main()
