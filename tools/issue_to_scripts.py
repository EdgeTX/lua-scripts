"""
Parse a GitHub Issue Form body and insert or update an entry in scripts.json.

Usage:
    uv run tools/issue_to_scripts.py \\
        --issue-body <path>     path to file containing the issue body markdown
        --scripts-json <path>   path to scripts.json (modified in place)
        --mode insert           insert a new entry (default)
        --mode patch            update fields on an existing entry

Exit codes:
    0  success
    1  validation / not-found / duplicate error
    2  file I/O error
"""

import argparse
import json
import re
import sys
from pathlib import Path

VALID_CATEGORIES = {
    "Audio & Media",
    "Flight Controller Config",
    "Games & Fun",
    "GPS & Mapping",
    "Logging & Analysis",
    "Radio Tools",
    "Telemetry & Widgets",
}

_NO_RESPONSE = "_no response_"


# ── Parsing ────────────────────────────────────────────────────────────────────

def parse_issue_body(text: str) -> dict[str, str]:
    """Split the issue form markdown into {heading: content} pairs."""
    sections: dict[str, str] = {}
    current_heading: str | None = None
    lines_buf: list[str] = []

    for line in text.splitlines():
        if line.startswith("### "):
            if current_heading is not None:
                sections[current_heading] = "\n".join(lines_buf).strip()
            current_heading = line[4:].strip()
            lines_buf = []
        elif current_heading is not None:
            lines_buf.append(line)

    if current_heading is not None:
        sections[current_heading] = "\n".join(lines_buf).strip()

    return sections


def _is_empty(value: str) -> bool:
    return not value or value.lower() == _NO_RESPONSE


def extract_checkboxes(text: str) -> list[str]:
    """Return labels of checked checkboxes."""
    checked = []
    for line in text.splitlines():
        m = re.match(r"^- \[x\]\s+(.+)$", line.strip(), re.IGNORECASE)
        if m:
            checked.append(m.group(1).strip())
    return checked


def extract_image_urls(text: str) -> list[str]:
    """Return valid http(s) URLs from a newline-separated textarea."""
    if _is_empty(text):
        return []
    return [
        line.strip()
        for line in text.splitlines()
        if line.strip().startswith(("http://", "https://"))
    ]


def extract_extra_tags(text: str) -> list[str]:
    """Parse comma-separated additional tags into a normalised list."""
    if _is_empty(text):
        return []
    return [t.strip().lower() for t in text.split(",") if t.strip()]


def build_tags(sections: dict[str, str]) -> list[str] | None:
    """
    Return the combined tag list, or None if the submitter left tags entirely
    untouched (no checkboxes checked and no extra tags — patch mode only).
    """
    checked = extract_checkboxes(sections.get("Tags", ""))
    extra = extract_extra_tags(sections.get("Additional Tags", ""))
    if not checked and not extra:
        return None
    seen: set[str] = set()
    tags: list[str] = []
    for tag in checked + extra:
        if tag not in seen:
            seen.add(tag)
            tags.append(tag)
    return tags


# ── Insert mode ────────────────────────────────────────────────────────────────

def build_insert_entry(sections: dict[str, str]) -> dict:
    """Validate sections and return a complete scripts.json entry."""
    name = sections.get("Script Name", "").strip()
    if not name:
        raise ValueError("Script Name is required.")

    category = sections.get("Category", "").strip()
    if category not in VALID_CATEGORIES:
        raise ValueError(
            f"Category '{category}' is not valid. Must be one of: {sorted(VALID_CATEGORIES)}"
        )

    description = sections.get("Description", "").strip()
    if _is_empty(description):
        raise ValueError("Description is required.")

    infourl = sections.get("Info URL", "").strip()
    if not infourl or not infourl.startswith(("http://", "https://")):
        raise ValueError(f"Info URL must start with http:// or https://: {infourl!r}")

    images = extract_image_urls(sections.get("Image URLs", ""))
    tags = build_tags(sections) or []

    return {
        "name": name,
        "category": category,
        "description": description,
        "infourl": infourl,
        "images": images,
        "tags": tags,
    }


def do_insert(scripts: list, new_entry: dict) -> list:
    """Insert new_entry after the last existing entry in the same category."""
    target_lower = new_entry["name"].lower()
    for existing in scripts:
        if existing.get("name", "").lower() == target_lower:
            raise ValueError(
                f"Duplicate: an entry named '{existing['name']}' already exists in scripts.json."
            )

    insert_after = -1
    for i, entry in enumerate(scripts):
        if entry.get("category") == new_entry["category"]:
            insert_after = i

    result = list(scripts)
    if insert_after == -1:
        result.append(new_entry)
    else:
        result.insert(insert_after + 1, new_entry)
    return result


# ── Patch mode ─────────────────────────────────────────────────────────────────

def do_patch(scripts: list, sections: dict[str, str]) -> tuple[list, dict]:
    """
    Update fields on the entry matching the submitted Script Name.
    Returns (updated_list, patched_entry).
    """
    lookup = sections.get("Script Name", "").strip()
    if not lookup:
        raise ValueError("Script Name is required to identify the entry to update.")

    target_idx = next(
        (i for i, e in enumerate(scripts) if e.get("name", "").lower() == lookup.lower()),
        None,
    )
    if target_idx is None:
        raise ValueError(
            f"No entry named '{lookup}' found in scripts.json. "
            "Check the name matches exactly (case-insensitive)."
        )

    entry = dict(scripts[target_idx])

    raw_category = sections.get("Category", "").strip()
    if raw_category and not _is_empty(raw_category):
        if raw_category not in VALID_CATEGORIES:
            raise ValueError(
                f"Category '{raw_category}' is not valid. Must be one of: {sorted(VALID_CATEGORIES)}"
            )
        entry["category"] = raw_category

    raw_description = sections.get("Description", "").strip()
    if not _is_empty(raw_description):
        entry["description"] = raw_description

    raw_infourl = sections.get("Info URL", "").strip()
    if not _is_empty(raw_infourl):
        if not raw_infourl.startswith(("http://", "https://")):
            raise ValueError(f"Info URL must start with http:// or https://: {raw_infourl!r}")
        entry["infourl"] = raw_infourl

    raw_images = sections.get("Image URLs", "")
    if not _is_empty(raw_images):
        urls = extract_image_urls(raw_images)
        if urls:
            entry["images"] = urls

    new_tags = build_tags(sections)
    if new_tags is not None:
        entry["tags"] = new_tags

    result = list(scripts)
    result[target_idx] = entry
    return result, entry


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--issue-body", type=Path, required=True,
                        help="Path to file containing the issue body markdown")
    parser.add_argument("--scripts-json", type=Path, default=Path("scripts.json"),
                        help="Path to scripts.json (modified in place)")
    parser.add_argument("--mode", choices=["insert", "patch"], default="insert",
                        help="insert: add a new entry; patch: update an existing entry")
    args = parser.parse_args()

    try:
        body_text = args.issue_body.read_text(encoding="utf-8")
    except OSError as e:
        print(f"Error reading issue body: {e}", file=sys.stderr)
        sys.exit(2)

    try:
        with open(args.scripts_json, encoding="utf-8") as f:
            scripts = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Error reading scripts.json: {e}", file=sys.stderr)
        sys.exit(2)

    sections = parse_issue_body(body_text)

    try:
        if args.mode == "insert":
            new_entry = build_insert_entry(sections)
            updated = do_insert(scripts, new_entry)
            result_entry = new_entry
        else:
            updated, result_entry = do_patch(scripts, sections)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        content = json.dumps(updated, indent=2, ensure_ascii=False) + "\n"
        args.scripts_json.write_text(content, encoding="utf-8")
    except OSError as e:
        print(f"Error writing scripts.json: {e}", file=sys.stderr)
        sys.exit(2)

    action = "Added" if args.mode == "insert" else "Updated"
    print(f"{action} '{result_entry['name']}' in {args.scripts_json}")
    print(json.dumps(result_entry, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
