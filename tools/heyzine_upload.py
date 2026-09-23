#!/usr/bin/env python3
"""
Post published campaign PDFs to Heyzine and record the flipbook links.

Heyzine's API does not accept file uploads — it fetches a publicly reachable URL.
So every PDF must already be committed and served by GitHub Pages before this runs.

The API key is read from the HEYZINE_API_KEY environment variable and is never
printed, logged or written to the manifest.

    export HEYZINE_API_KEY=...        # do not paste this into a chat transcript
    python3 tools/heyzine_upload.py --dry-run
    python3 tools/heyzine_upload.py

Re-running is safe: anything already in the manifest is skipped unless --force.
"""

import argparse
import json
import os
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request

REPO = pathlib.Path(__file__).resolve().parent.parent
DOCS = REPO / "documents"
MANIFEST = REPO / "tools" / "heyzine-flipbooks.json"
BASE_URL = "https://apertureglobal.github.io/marketing"
ENDPOINT = "https://heyzine.com/api1/rest"


def public_url(pdf: pathlib.Path) -> str:
    """Repo-relative path -> the Pages URL, each path segment encoded separately
    so spaces and accented characters survive but the slashes do not."""
    rel = pdf.relative_to(REPO)
    return BASE_URL + "/" + "/".join(
        urllib.parse.quote(part, safe="") for part in rel.parts
    )


def describe(pdf: pathlib.Path) -> tuple[str, str]:
    """('Aperture Billboard Strategy - 312 Madison St', 'Alex Brandau IV')"""
    agent = pdf.relative_to(DOCS).parts[0]
    return pdf.stem, agent


def reachable(url: str) -> bool:
    req = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status == 200
    except Exception:
        return False


def create_flipbook(api_key: str, url: str, title: str, subtitle: str) -> dict:
    payload = urllib.parse.urlencode(
        {"pdf": url, "title": title, "subtitle": subtitle}
    ).encode()
    req = urllib.request.Request(
        ENDPOINT,
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="show what would be posted, check the URLs resolve, send nothing")
    ap.add_argument("--force", action="store_true",
                    help="re-post PDFs already recorded in the manifest")
    args = ap.parse_args()

    api_key = os.environ.get("HEYZINE_API_KEY", "").strip()
    if not api_key and not args.dry_run:
        print("HEYZINE_API_KEY is not set. Export it and re-run "
              "(or use --dry-run to check the URLs first).", file=sys.stderr)
        return 1

    manifest = {}
    if MANIFEST.exists():
        manifest = json.loads(MANIFEST.read_text())

    pdfs = sorted(DOCS.rglob("*.pdf"))
    if not pdfs:
        print(f"No PDFs under {DOCS}", file=sys.stderr)
        return 1

    unreachable, posted, skipped, failed = [], 0, 0, 0

    for pdf in pdfs:
        key = str(pdf.relative_to(REPO))
        title, agent = describe(pdf)
        url = public_url(pdf)

        if key in manifest and not args.force:
            skipped += 1
            continue

        ok = reachable(url)
        status = "ok" if ok else "NOT REACHABLE"
        print(f"{status:>14}  {title}")
        if not ok:
            unreachable.append(url)
            continue

        if args.dry_run:
            continue

        try:
            result = create_flipbook(api_key, url, title, agent)
        except urllib.error.HTTPError as e:
            print(f"         FAILED  {title}: HTTP {e.code} {e.read().decode()[:200]}",
                  file=sys.stderr)
            failed += 1
            continue

        manifest[key] = {
            "title": title,
            "agent": agent,
            "pdf_url": url,
            "flipbook": result.get("url") or result.get("link"),
            "raw": result,
        }
        print(f"      flipbook  {manifest[key]['flipbook']}")
        posted += 1

    if not args.dry_run and posted:
        MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
        print(f"\nManifest written: {MANIFEST.relative_to(REPO)}")

    print(f"\n{len(pdfs)} PDFs — posted {posted}, skipped {skipped} "
          f"(already done), failed {failed}, unreachable {len(unreachable)}")

    if unreachable:
        print("\nNot reachable yet — these must be committed, pushed, and served "
              "by Pages before Heyzine can fetch them:", file=sys.stderr)
        for u in unreachable:
            print(f"  {u}", file=sys.stderr)
        return 2

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
