#!/usr/bin/env python3
"""
Validate scripts.json against the expected schema.

Exit 0 = valid, Exit 1 = errors found.
"""

import argparse
import json
import sys
from pathlib import Path

KNOWN_CATEGORIES = {
    "Audio & Media",
    "Flight Controller Config",
    "Games & Fun",
    "GPS & Mapping",
    "Logging & Analysis",
    "Radio Tools",
    "Telemetry & Widgets",
}

REQUIRED_FIELDS = ["name", "category", "description", "infourl", "images", "tags"]
STRING_FIELDS = ["name", "category", "description", "infourl"]


def load_and_parse(path: Path) -> list:
    if not path.exists():
        print(f"Error: {path} not found", file=sys.stderr)
        sys.exit(1)
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON in {path}: {e}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(data, list):
        print(f"Error: {path} must be a JSON array", file=sys.stderr)
        sys.exit(1)
    return data


def validate(data: list) -> list[str]:
    errors = []
    seen_names: dict[str, int] = {}

    for i, entry in enumerate(data):
        prefix = f"Entry {i}"

        if not isinstance(entry, dict):
            errors.append(f"{prefix}: not an object")
            continue

        for field in REQUIRED_FIELDS:
            if field not in entry:
                errors.append(f"{prefix}: missing required field '{field}'")

        for field in STRING_FIELDS:
            if field in entry:
                if not isinstance(entry[field], str) or not entry[field].strip():
                    errors.append(f"{prefix}: '{field}' must be a non-empty string")

        category = entry.get("category")
        if isinstance(category, str) and category.strip() and category not in KNOWN_CATEGORIES:
            errors.append(
                f"{prefix}: unknown category '{category}'"
                f" (known: {sorted(KNOWN_CATEGORIES)})"
            )

        infourl = entry.get("infourl")
        if isinstance(infourl, str) and infourl.strip():
            if not (infourl.startswith("http://") or infourl.startswith("https://")):
                errors.append(f"{prefix}: 'infourl' must start with http:// or https://")

        if "images" in entry and not isinstance(entry["images"], list):
            errors.append(f"{prefix}: 'images' must be a list")

        if "tags" in entry and not isinstance(entry["tags"], list):
            errors.append(f"{prefix}: 'tags' must be a list")

        name = entry.get("name")
        if isinstance(name, str) and name.strip():
            key = name.strip().lower()
            if key in seen_names:
                errors.append(
                    f"{prefix}: duplicate name '{name}'"
                    f" (also at entry {seen_names[key]})"
                )
            else:
                seen_names[key] = i

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate scripts.json schema")
    parser.add_argument(
        "--scripts-json",
        default="scripts.json",
        type=Path,
        help="Path to scripts.json (default: scripts.json)",
    )
    args = parser.parse_args()

    data = load_and_parse(args.scripts_json)
    errors = validate(data)

    if errors:
        print(f"Found {len(errors)} error(s) in {args.scripts_json}:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

    print(f"{args.scripts_json} is valid ({len(data)} entries).")


if __name__ == "__main__":
    main()
