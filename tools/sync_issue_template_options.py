#!/usr/bin/env python3
"""
Keep the "Category" dropdown and "Tags" checkboxes in the Issue Form templates
(.github/ISSUE_TEMPLATE/add-script.yml, update-script.yml) in sync with
scripts.schema.json, which in turn tracks actual usage in scripts.json.

Tags are a pure snapshot of current usage in scripts.json (a tag that stops
being used drops out on the next --write). Categories are monotonic add-only:
new categories used in scripts.json get promoted, but a category already known
is never removed just because it currently has zero entries — see the plan
this script was built from for why (categories drive the gallery's top-level
navigation tabs, and dropping one from the dropdown just because it's briefly
empty would be actively unhelpful). Pass --prune-categories to deliberately
override that and remove currently-unused categories too.

Usage:
    uv run tools/sync_issue_template_options.py --check
    uv run tools/sync_issue_template_options.py --write
    uv run tools/sync_issue_template_options.py --check --prune-categories
    uv run tools/sync_issue_template_options.py --write --prune-categories

Exit codes:
    0  in sync (--check) or write completed/no-op (--write)
    1  drift found (--check only)
    2  file I/O error, malformed scripts.schema.json, or missing markers
"""

import argparse
import difflib
import json
import re
import sys
from pathlib import Path

TAG_BEGIN = "# --- BEGIN AUTO-GENERATED TAGS (see scripts.schema.json: items.properties.tags.items.examples) ---"
TAG_END = "# --- END AUTO-GENERATED TAGS ---"
CATEGORY_BEGIN = "# --- BEGIN AUTO-GENERATED CATEGORIES (see scripts.schema.json: items.properties.category.examples) ---"
CATEGORY_END = "# --- END AUTO-GENERATED CATEGORIES ---"

DEFAULT_TEMPLATES = [
    Path(".github/ISSUE_TEMPLATE/add-script.yml"),
    Path(".github/ISSUE_TEMPLATE/update-script.yml"),
]

TAG_ITEM_RE = re.compile(r"^\s*-\s*label:\s*(.+?)\s*$")
CATEGORY_ITEM_RE = re.compile(r"^\s*-\s*(.+?)\s*$")


# ── Loading ──────────────────────────────────────────────────────────────────

def load_scripts_json(path: Path) -> list:
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Error: unable to read/parse {path}: {e}", file=sys.stderr)
        sys.exit(2)
    if not isinstance(data, list):
        print(f"Error: {path} must be a JSON array", file=sys.stderr)
        sys.exit(2)
    return data


def load_schema(path: Path) -> dict:
    try:
        with open(path, encoding="utf-8") as f:
            schema = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Error: unable to read/parse {path}: {e}", file=sys.stderr)
        sys.exit(2)
    try:
        schema["items"]["properties"]["category"]
        schema["items"]["properties"]["tags"]["items"]
    except (KeyError, TypeError) as e:
        print(
            f"Error: {path} missing items.properties.category / "
            f"items.properties.tags.items: {e}",
            file=sys.stderr,
        )
        sys.exit(2)
    return schema


def get_schema_examples(schema: dict, field: str) -> list[str]:
    """field: 'category' or 'tags'."""
    if field == "category":
        node = schema["items"]["properties"]["category"]
    else:
        node = schema["items"]["properties"]["tags"]["items"]
    examples = node.get("examples", [])
    if not isinstance(examples, list) or not all(isinstance(x, str) for x in examples):
        print(
            f"Error: scripts.schema.json items.properties.{field} examples "
            "must be a list of strings",
            file=sys.stderr,
        )
        sys.exit(2)
    return examples


def set_schema_examples(schema: dict, field: str, values: list[str]) -> None:
    if field == "category":
        schema["items"]["properties"]["category"]["examples"] = values
    else:
        schema["items"]["properties"]["tags"]["items"]["examples"] = values


def save_schema(path: Path, schema: dict) -> None:
    try:
        path.write_text(json.dumps(schema, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    except OSError as e:
        print(f"Error: unable to write {path}: {e}", file=sys.stderr)
        sys.exit(2)


# ── Computation ──────────────────────────────────────────────────────────────

def _sort(values) -> list[str]:
    """Case-insensitive sort — plain sorted() would put e.g. 'GPS & Mapping'
    before 'Games & Fun' (uppercase 'P' < lowercase 'a' in ASCII), which
    isn't the order a human reading the dropdown/checkbox list would expect."""
    return sorted(values, key=str.casefold)


def compute(scripts: list, schema: dict, prune_categories: bool = False) -> dict:
    current_tags = _sort({tag for e in scripts for tag in e.get("tags", []) if isinstance(tag, str)})

    used_categories = _sort({
        e["category"] for e in scripts
        if isinstance(e.get("category"), str) and e["category"].strip()
    })
    previous_categories = get_schema_examples(schema, "category")
    if prune_categories:
        # Deliberate override of the normal monotonic-add-only behavior —
        # only takes effect when explicitly requested (--prune-categories).
        current_categories = used_categories
    else:
        current_categories = _sort(set(previous_categories) | set(used_categories))
    new_categories = _sort(set(used_categories) - set(previous_categories))
    unused_categories = _sort(set(current_categories) - set(used_categories))

    return {
        "current_tags": current_tags,
        "current_categories": current_categories,
        "new_categories": new_categories,
        "unused_categories": unused_categories,
    }


# ── Marker-bounded block handling ───────────────────────────────────────────

def find_block(lines: list[str], begin: str, end: str, path: Path, block_name: str) -> tuple[int, int]:
    begin_idx = next((i for i, line in enumerate(lines) if line.strip() == begin), None)
    end_idx = next((i for i, line in enumerate(lines) if line.strip() == end), None)
    if begin_idx is None or end_idx is None or end_idx <= begin_idx:
        print(
            f"Error: {path} is missing the {block_name} marker pair "
            f"({begin!r} / {end!r})",
            file=sys.stderr,
        )
        sys.exit(2)
    return begin_idx, end_idx


def block_indent(lines: list[str], begin_idx: int) -> str:
    marker_line = lines[begin_idx]
    return marker_line[: len(marker_line) - len(marker_line.lstrip())]


def render_tag_lines(indent: str, tags: list[str]) -> list[str]:
    return [f"{indent}- label: {tag}" for tag in tags]


def render_category_lines(indent: str, categories: list[str]) -> list[str]:
    return [f"{indent}- {category}" for category in categories]


def parse_block_values(lines: list[str], begin_idx: int, end_idx: int, item_re: re.Pattern) -> list[str]:
    values = []
    for line in lines[begin_idx + 1:end_idx]:
        m = item_re.match(line)
        if m:
            values.append(m.group(1).strip())
    return values


def rewrite_lines(lines: list[str], blocks: list[tuple[int, int, list[str]]]) -> list[str]:
    """Apply multiple (begin_idx, end_idx, replacement_lines) edits in one pass,
    computed against the original `lines` — never mutate indices between edits."""
    blocks = sorted(blocks, key=lambda b: b[0])
    result: list[str] = []
    cursor = 0
    for begin_idx, end_idx, replacement in blocks:
        result.extend(lines[cursor:begin_idx + 1])
        result.extend(replacement)
        result.append(lines[end_idx])
        cursor = end_idx + 1
    result.extend(lines[cursor:])
    return result


def compute_template_blocks(
    template_path: Path, current_tags: list[str], current_categories: list[str]
) -> tuple[list[str], list[tuple[int, int, list[str], str, list[str]]]]:
    """Returns (original_lines, [(begin_idx, end_idx, expected_replacement, block_name, actual_values), ...])."""
    try:
        text = template_path.read_text(encoding="utf-8")
    except OSError as e:
        print(f"Error: unable to read {template_path}: {e}", file=sys.stderr)
        sys.exit(2)
    lines = text.splitlines()

    tag_begin, tag_end = find_block(lines, TAG_BEGIN, TAG_END, template_path, "tags")
    cat_begin, cat_end = find_block(lines, CATEGORY_BEGIN, CATEGORY_END, template_path, "category")

    tag_indent = block_indent(lines, tag_begin)
    cat_indent = block_indent(lines, cat_begin)

    tag_actual = parse_block_values(lines, tag_begin, tag_end, TAG_ITEM_RE)
    cat_actual = parse_block_values(lines, cat_begin, cat_end, CATEGORY_ITEM_RE)

    blocks = [
        (tag_begin, tag_end, render_tag_lines(tag_indent, current_tags), "tags", tag_actual),
        (cat_begin, cat_end, render_category_lines(cat_indent, current_categories), "category", cat_actual),
    ]
    return lines, blocks


def check_template(template_path: Path, current_tags: list[str], current_categories: list[str]) -> list[str]:
    """Returns a list of human-readable issue descriptions (empty if in sync)."""
    lines, blocks = compute_template_blocks(template_path, current_tags, current_categories)
    issues = []
    for begin_idx, end_idx, expected, block_name, actual in blocks:
        expected_values = current_tags if block_name == "tags" else current_categories
        if actual == expected_values:
            continue
        missing = _sort(set(expected_values) - set(actual))
        extra = _sort(set(actual) - set(expected_values))
        diff = "\n".join(
            difflib.unified_diff(
                lines[begin_idx:end_idx + 1],
                [lines[begin_idx]] + expected + [lines[end_idx]],
                fromfile=f"{template_path} [{block_name}] (current)",
                tofile=f"{template_path} [{block_name}] (expected)",
                lineterm="",
            )
        )
        issues.append(
            f"{template_path} [{block_name}]: out of sync\n"
            f"  missing: {missing}\n"
            f"  extra:   {extra}\n"
            f"{diff}"
        )
    return issues


def write_template(template_path: Path, current_tags: list[str], current_categories: list[str]) -> bool:
    """Returns True if the file changed."""
    lines, blocks = compute_template_blocks(template_path, current_tags, current_categories)
    rewrite_blocks = [(b, e, replacement) for b, e, replacement, _, _ in blocks]
    new_lines = rewrite_lines(lines, rewrite_blocks)
    new_text = "\n".join(new_lines) + "\n"
    old_text = template_path.read_text(encoding="utf-8")
    if new_text == old_text:
        return False
    try:
        template_path.write_text(new_text, encoding="utf-8")
    except OSError as e:
        print(f"Error: unable to write {template_path}: {e}", file=sys.stderr)
        sys.exit(2)
    return True


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--scripts-json", default=Path("scripts.json"), type=Path)
    parser.add_argument("--schema", default=Path("scripts.schema.json"), type=Path)
    parser.add_argument("--templates", nargs="+", type=Path, default=DEFAULT_TEMPLATES)
    parser.add_argument(
        "--prune-categories", action="store_true",
        help=(
            "Also remove categories with zero current entries in scripts.json, "
            "overriding the normal monotonic-add-only behavior. Use deliberately "
            "(e.g. after confirming a category should be retired) — combine with "
            "--check first to preview what would be pruned."
        ),
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="Exit 1 if anything is out of sync")
    mode.add_argument("--write", action="store_true", help="Regenerate schema examples and template blocks in place")
    args = parser.parse_args()

    scripts = load_scripts_json(args.scripts_json)
    schema = load_schema(args.schema)
    computed = compute(scripts, schema, prune_categories=args.prune_categories)
    current_tags = computed["current_tags"]
    current_categories = computed["current_categories"]

    if args.check:
        issues = []

        # Direct (order-sensitive) comparison, not sorted() on both sides —
        # the schema's examples arrays are always supposed to already hold
        # the canonical _sort()-ordered list, so a stale *order* on disk
        # (e.g. written before a sort-key change) must count as drift too,
        # not just a stale *set* of values.
        schema_tags = get_schema_examples(schema, "tags")
        if schema_tags != current_tags:
            issues.append(
                f"{args.schema} [tags.examples]: out of sync\n"
                f"  missing: {_sort(set(current_tags) - set(schema_tags))}\n"
                f"  extra:   {_sort(set(schema_tags) - set(current_tags))}"
            )
        schema_categories = get_schema_examples(schema, "category")
        if schema_categories != current_categories:
            issues.append(
                f"{args.schema} [category.examples]: out of sync\n"
                f"  missing: {_sort(set(current_categories) - set(schema_categories))}\n"
                f"  extra:   {_sort(set(schema_categories) - set(current_categories))}"
            )

        for template_path in args.templates:
            issues.extend(check_template(template_path, current_tags, current_categories))

        if issues:
            print(f"Found {len(issues)} out-of-sync region(s):")
            for issue in issues:
                print(issue)
                print()
            sys.exit(1)

        print("All tags/category regions are in sync.")
        return

    # --write
    changed_anything = False

    schema_tags = get_schema_examples(schema, "tags")
    schema_categories = get_schema_examples(schema, "category")
    if schema_tags != current_tags or schema_categories != current_categories:
        set_schema_examples(schema, "tags", current_tags)
        set_schema_examples(schema, "category", current_categories)
        save_schema(args.schema, schema)
        changed_anything = True
        print(f"Updated {args.schema}")

    for template_path in args.templates:
        if write_template(template_path, current_tags, current_categories):
            changed_anything = True
            print(f"Updated {template_path}")

    if computed["new_categories"]:
        print(f"new_categories={','.join(computed['new_categories'])}")
    if computed["unused_categories"]:
        print(f"unused_categories={','.join(computed['unused_categories'])}")

    if not changed_anything:
        print("Already in sync, nothing written.")


if __name__ == "__main__":
    main()
