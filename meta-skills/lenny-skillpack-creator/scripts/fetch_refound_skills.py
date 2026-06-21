#!/usr/bin/env python3

"""
fetch_refound_skills.py

Download Refound/Lenny skills (SKILL.md) in batch.

It will:
1) Fetch the browse page to discover skill slugs
2) For each slug, try downloading the Agent Skill file:
      https://refoundai.com/skills/<slug>/SKILL.md
   If that fails, it will save the HTML skill page as a fallback:
      https://refoundai.com/lenny-skills/s/<slug>/

Usage:
  python scripts/fetch_refound_skills.py --out ./lenny-src
Optional:
  --browse-url https://refoundai.com/lenny-skills/browse/
  --limit 10
  --sleep 0.2

Notes:
- This script requires internet access and the 'requests' package.
- Use responsibly; respect the website’s terms.
"""

from __future__ import annotations
import argparse
import re
import time
from pathlib import Path

try:
    import requests  # type: ignore
except Exception as e:  # pragma: no cover
    raise SystemExit("This script requires 'requests'. Install via: pip install requests") from e

DEFAULT_BROWSE = "https://refoundai.com/lenny-skills/browse/"
SKILL_PAGE_PREFIX = "https://refoundai.com/lenny-skills/s/"
SKILL_MD_PREFIX = "https://refoundai.com/skills/"

# Browse pages often render links like:
#   href="/lenny-skills/s/<slug>" class="..."
# The previous regex was too permissive and could accidentally capture
# HTML attributes until the next "/" (e.g., from a closing tag).
SLUG_RE = re.compile(
    r"""href=["'](?:https?://refoundai\.com)?/lenny-skills/s/([^"'/\s?#>]+)""",
    flags=re.IGNORECASE,
)

VALID_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

def discover_slugs(html: str) -> list[str]:
    slugs = SLUG_RE.findall(html)
    # preserve order, unique
    seen = set()
    out = []
    for s in slugs:
        s = s.strip().strip("/")
        if not VALID_SLUG_RE.match(s):
            # Keep going; this is best-effort discovery.
            print(f"[warn] skipping invalid slug candidate: {s!r}")
            continue
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out

def fetch(url: str, timeout: int = 30) -> requests.Response:
    return requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0 (skillpack-fetcher)"})

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True, help="Output directory to store downloaded SKILL.md files.")
    p.add_argument("--browse-url", default=DEFAULT_BROWSE)
    p.add_argument("--limit", type=int, default=0, help="If set, limit number of skills to download.")
    p.add_argument("--sleep", type=float, default=0.25, help="Sleep seconds between requests.")
    args = p.parse_args()

    out_dir = Path(args.out).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    r = fetch(args.browse_url)
    r.raise_for_status()
    slugs = discover_slugs(r.text)
    if args.limit and args.limit > 0:
        slugs = slugs[: args.limit]

    print(f"[info] discovered {len(slugs)} skill slugs")

    ok = 0
    saved_html = 0
    failed = 0
    for slug in slugs:
        skill_dir = out_dir / slug
        skill_dir.mkdir(parents=True, exist_ok=True)

        # Try SKILL.md
        md_url = f"{SKILL_MD_PREFIX}{slug}/SKILL.md"
        try:
            mr = fetch(md_url)
            if mr.status_code == 200 and mr.text.lstrip().startswith("---"):
                (skill_dir / "SKILL.md").write_text(mr.text, encoding="utf-8")
                ok += 1
                print(f"[ok] {slug} -> SKILL.md")
            else:
                raise RuntimeError(f"Unexpected status/content: {mr.status_code}")
        except Exception as e:
            # fallback to HTML page
            page_url = f"{SKILL_PAGE_PREFIX}{slug}/"
            try:
                pr = fetch(page_url)
                if pr.status_code != 200:
                    raise RuntimeError(f"Fallback page returned {pr.status_code}")
                (skill_dir / "page.html").write_text(pr.text, encoding="utf-8")
                saved_html += 1
                print(f"[warn] {slug} -> saved HTML fallback (SKILL.md download failed)")
            except Exception as fallback_err:
                failed += 1
                (skill_dir / "fetch_error.txt").write_text(
                    f"SKILL.md url: {md_url}\n"
                    f"SKILL.md error: {type(e).__name__}: {e}\n"
                    f"HTML url: {page_url}\n"
                    f"HTML error: {type(fallback_err).__name__}: {fallback_err}\n",
                    encoding="utf-8",
                )
                print(f"[error] {slug} -> failed to download SKILL.md and HTML fallback; wrote fetch_error.txt")

        time.sleep(max(0.0, float(args.sleep)))

    print(
        f"[done] SKILL.md downloaded: {ok}/{len(slugs)} "
        f"(html fallback: {saved_html}, failed: {failed})"
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
