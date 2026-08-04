#!/usr/bin/env python3
"""
Download external image URLs referenced in scripts.json (e.g. raw GitHub
URLs submitted via the issue form) into ASSETS/<slug>/, and rewrite
scripts.json to point at the local copies instead.

Only entries with at least one http(s):// image are touched; entries already
fully local are left alone. If an entry already has local ASSETS/ images,
its existing slug (taken from those paths) is reused rather than recomputed
from the current name, so a renamed entry doesn't end up split across two
directories.

Usage:
    uv run tools/download_external_images.py                  # all entries
    uv run tools/download_external_images.py --name "Some App" # one entry
    uv run tools/download_external_images.py --dry-run         # preview only

Note: --dry-run still fetches each URL (read-only) to determine its file
extension, since some URLs (e.g. GitHub's issue-attachment upload links)
have no extension in the path and can only be identified from the response's
Content-Type. Nothing is ever written to disk or to scripts.json in dry-run.

Exit codes:
    0  success (including nothing to do)
    1  one or more images failed to download (partial progress kept for
       entries that fully succeeded; a failed entry is left untouched)
    2  file I/O / argument error
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}
CONTENT_TYPE_EXTENSIONS = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/gif": ".gif",
    "image/webp": ".webp",
    "image/svg+xml": ".svg",
}
SCREENSHOT_RE = re.compile(r"^screenshot-(\d+)\.\w+$")
USER_AGENT = "lua-scripts-download-external-images/1.0"


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9\s-]", "", name.lower())
    slug = re.sub(r"[\s_]+", "-", slug)
    return re.sub(r"-+", "-", slug).strip("-")


def entry_slug(entry: dict) -> str:
    for img in entry.get("images", []):
        if img.startswith("ASSETS/"):
            return img.split("/")[1]
    return slugify(entry["name"])


def next_screenshot_number(assets_dir: Path, slug: str) -> int:
    folder = assets_dir / slug
    if not folder.is_dir():
        return 1
    numbers = []
    for f in folder.iterdir():
        m = SCREENSHOT_RE.match(f.name)
        if m:
            numbers.append(int(m.group(1)))
    return max(numbers, default=0) + 1


def guess_extension_from_url(url: str) -> str | None:
    suffix = Path(urlparse(url).path).suffix.lower()
    return suffix if suffix in IMAGE_EXTENSIONS else None


def fetch_with_extension(url: str, timeout: float) -> tuple[str, bytes]:
    """
    Download the URL and return (extension, data). Extension is taken from
    the URL path if recognized, otherwise sniffed from the response's
    Content-Type header — GitHub's issue-attachment upload URLs
    (github.com/user-attachments/assets/<uuid>) have no file extension in
    the path at all, so the URL alone isn't always enough.
    """
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        data = response.read()
        ext = guess_extension_from_url(url)
        if ext is None:
            content_type = response.headers.get("Content-Type", "").split(";")[0].strip().lower()
            ext = CONTENT_TYPE_EXTENSIONS.get(content_type)
    if not data:
        raise ValueError("empty response body")
    if ext is None:
        raise ValueError("could not determine an image extension from the URL or Content-Type")
    return ext, data


def process_entry(entry: dict, assets_dir: Path, dry_run: bool, timeout: float) -> tuple[bool, list[str]]:
    """Returns (changed, errors). Leaves entry untouched if any download fails."""
    images = entry.get("images", [])
    url_indices = [i for i, img in enumerate(images) if img.startswith(("http://", "https://"))]
    if not url_indices:
        return False, []

    slug = entry_slug(entry)
    next_n = next_screenshot_number(assets_dir, slug)
    new_images = list(images)
    downloaded: list[Path] = []
    errors: list[str] = []

    for i in url_indices:
        url = images[i]
        try:
            # Dry-run still fetches (read-only, nothing written) since an
            # extension-less URL genuinely can't be previewed without it.
            ext, data = fetch_with_extension(url, timeout)
        except (urllib.error.URLError, TimeoutError, ValueError, OSError) as e:
            errors.append(f"{url}: {e}")
            break
        local_path = f"ASSETS/{slug}/screenshot-{next_n}{ext}"
        if dry_run:
            print(f"  would download {url} -> {local_path}")
        else:
            dest = assets_dir / slug / f"screenshot-{next_n}{ext}"
            try:
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(data)
                downloaded.append(dest)
            except OSError as e:
                errors.append(f"{url}: {e}")
                break
        new_images[i] = local_path
        next_n += 1

    if errors:
        # Roll back any files this entry's run created — keep it all-or-nothing
        # per entry so a partial failure doesn't leave a half-migrated set.
        for f in downloaded:
            f.unlink(missing_ok=True)
        return False, errors

    if not dry_run:
        entry["images"] = new_images
    return True, []


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--scripts-json", default=Path("scripts.json"), type=Path)
    parser.add_argument("--assets-dir", default=Path("ASSETS"), type=Path)
    parser.add_argument("--name", help="Only process the entry with this exact name (case-insensitive)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without downloading or writing files")
    parser.add_argument("--timeout", type=float, default=15.0, help="Per-image download timeout in seconds")
    args = parser.parse_args()

    try:
        with open(args.scripts_json, encoding="utf-8") as f:
            scripts = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Error: unable to read {args.scripts_json}: {e}", file=sys.stderr)
        sys.exit(2)

    if args.name:
        targets = [e for e in scripts if e.get("name", "").lower() == args.name.lower()]
        if not targets:
            print(f"Error: no entry named '{args.name}' found in {args.scripts_json}", file=sys.stderr)
            sys.exit(2)
    else:
        targets = scripts

    any_changed = False
    any_errors = False

    for entry in targets:
        images = entry.get("images", [])
        if not any(img.startswith(("http://", "https://")) for img in images):
            continue
        print(f"{entry.get('name', '?')}:")
        changed, errors = process_entry(entry, args.assets_dir, args.dry_run, args.timeout)
        if errors:
            any_errors = True
            for err in errors:
                print(f"  Error: {err}", file=sys.stderr)
            print("  Skipped (no changes applied to this entry).")
        elif changed:
            any_changed = True
            if args.dry_run:
                print("  (dry run, nothing written)")
            else:
                for img in entry["images"]:
                    print(f"  -> {img}")

    if any_changed and not args.dry_run:
        try:
            content = json.dumps(scripts, indent=2, ensure_ascii=False) + "\n"
            args.scripts_json.write_text(content, encoding="utf-8")
        except OSError as e:
            print(f"Error: unable to write {args.scripts_json}: {e}", file=sys.stderr)
            sys.exit(2)
        print(f"Updated {args.scripts_json}")

    if not any_changed and not any_errors:
        print("Nothing to do — no external image URLs found.")

    sys.exit(1 if any_errors else 0)


if __name__ == "__main__":
    main()
