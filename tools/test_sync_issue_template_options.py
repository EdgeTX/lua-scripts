#!/usr/bin/env python3
"""
Tests for tools/sync_issue_template_options.py — the multi-region marker
splicing and monotonic-add category logic are fiddly enough to be worth
covering with something more than manual verification.

Usage:
    uv run tools/test_sync_issue_template_options.py
    python3 -m unittest tools/test_sync_issue_template_options.py
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parent / "sync_issue_template_options.py"

TEMPLATE_FIXTURE = """\
name: Test Template
body:
  - type: dropdown
    id: category
    attributes:
      options:
        # --- BEGIN AUTO-GENERATED CATEGORIES (see scripts.schema.json: items.properties.category.examples) ---
{category_lines}
        # --- END AUTO-GENERATED CATEGORIES ---
  - type: checkboxes
    id: tags_common
    attributes:
      options:
        # --- BEGIN AUTO-GENERATED TAGS (see scripts.schema.json: items.properties.tags.items.examples) ---
{tag_lines}
        # --- END AUTO-GENERATED TAGS ---
"""

TEMPLATE_NO_MARKERS = """\
name: Test Template
body:
  - type: dropdown
    id: category
    attributes:
      options:
        - Cat A
"""


def render_category_lines(categories: list[str]) -> str:
    return "\n".join(f"        - {c}" for c in categories)


def render_tag_lines(tags: list[str]) -> str:
    return "\n".join(f"        - label: {t}" for t in tags)


class SyncFixture:
    """Builds a scratch directory with scripts.json / scripts.schema.json /
    two template files, so tests never touch the real repo files."""

    def __init__(self, tmpdir: Path, entries: list[dict], schema_categories: list[str],
                 template_categories: list[str] | None = None,
                 template_tags: list[str] | None = None):
        self.dir = tmpdir
        self.scripts_json = tmpdir / "scripts.json"
        self.scripts_json.write_text(json.dumps(entries), encoding="utf-8")

        used_tags = sorted({t for e in entries for t in e.get("tags", [])})
        self.schema_json = tmpdir / "scripts.schema.json"
        schema = {
            "items": {
                "properties": {
                    "category": {"type": "string", "examples": schema_categories},
                    "tags": {"type": "array", "items": {"type": "string", "examples": used_tags}},
                }
            }
        }
        self.schema_json.write_text(json.dumps(schema), encoding="utf-8")

        tmpl_categories = template_categories if template_categories is not None else schema_categories
        tmpl_tags = template_tags if template_tags is not None else used_tags
        template_text = TEMPLATE_FIXTURE.format(
            category_lines=render_category_lines(tmpl_categories),
            tag_lines=render_tag_lines(tmpl_tags),
        )
        self.template_a = tmpdir / "template_a.yml"
        self.template_b = tmpdir / "template_b.yml"
        self.template_a.write_text(template_text, encoding="utf-8")
        self.template_b.write_text(template_text, encoding="utf-8")

    def run(self, *extra_args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [
                sys.executable, str(SCRIPT),
                "--scripts-json", str(self.scripts_json),
                "--schema", str(self.schema_json),
                "--templates", str(self.template_a), str(self.template_b),
                *extra_args,
            ],
            capture_output=True, text=True,
        )

    def schema_examples(self) -> tuple[list[str], list[str]]:
        schema = json.loads(self.schema_json.read_text(encoding="utf-8"))
        return schema["items"]["properties"]["tags"]["items"]["examples"], \
            schema["items"]["properties"]["category"]["examples"]


class TestSync(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmpdir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_check_in_sync(self):
        entries = [{"category": "Cat A", "tags": ["tag-a"]}]
        fx = SyncFixture(self.tmpdir, entries, schema_categories=["Cat A"])
        result = fx.run("--check")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("in sync", result.stdout)

    def test_check_detects_new_tag(self):
        entries = [{"category": "Cat A", "tags": ["tag-a", "tag-new"]}]
        fx = SyncFixture(self.tmpdir, entries, schema_categories=["Cat A"],
                          template_tags=["tag-a"])
        result = fx.run("--check")
        self.assertEqual(result.returncode, 1)
        self.assertIn("[tags]", result.stdout)

    def test_check_detects_new_category(self):
        entries = [{"category": "Cat B", "tags": ["tag-a"]}]
        fx = SyncFixture(self.tmpdir, entries, schema_categories=["Cat A"],
                          template_categories=["Cat A"])
        result = fx.run("--check")
        self.assertEqual(result.returncode, 1)
        self.assertIn("[category]", result.stdout)

    def test_write_promotes_new_tag_and_category(self):
        entries = [{"category": "Cat A", "tags": ["tag-a"]},
                   {"category": "Cat New", "tags": ["tag-new"]}]
        fx = SyncFixture(self.tmpdir, entries, schema_categories=["Cat A"],
                          template_categories=["Cat A"], template_tags=["tag-a"])
        result = fx.run("--write")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        tags, categories = fx.schema_examples()
        self.assertEqual(tags, ["tag-a", "tag-new"])
        self.assertEqual(categories, ["Cat A", "Cat New"])
        self.assertIn("- Cat New", fx.template_a.read_text())
        self.assertIn("- label: tag-new", fx.template_a.read_text())
        self.assertIn("new_categories=Cat New", result.stdout)

    def test_category_removal_is_monotonic(self):
        # Cat B is known (schema) but no entry currently uses it.
        entries = [{"category": "Cat A", "tags": ["tag-a"]}]
        fx = SyncFixture(self.tmpdir, entries, schema_categories=["Cat A", "Cat B"],
                          template_categories=["Cat A", "Cat B"])
        result = fx.run("--write")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        _, categories = fx.schema_examples()
        self.assertIn("Cat B", categories, "unused category must not be pruned automatically")
        self.assertIn("- Cat B", fx.template_a.read_text())
        self.assertIn("unused_categories=Cat B", result.stdout)

    def test_tag_removal_drops_from_checkboxes(self):
        # tag-old is in the schema/templates but no entry currently uses it.
        entries = [{"category": "Cat A", "tags": ["tag-a"]}]
        fx = SyncFixture(self.tmpdir, entries, schema_categories=["Cat A"],
                          template_tags=["tag-a", "tag-old"])
        # seed schema with tag-old too, so we can prove it gets dropped
        schema = json.loads(fx.schema_json.read_text())
        schema["items"]["properties"]["tags"]["items"]["examples"] = ["tag-a", "tag-old"]
        fx.schema_json.write_text(json.dumps(schema))

        result = fx.run("--write")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        tags, _ = fx.schema_examples()
        self.assertNotIn("tag-old", tags, "unused tag should drop out (unlike categories)")
        self.assertNotIn("tag-old", fx.template_a.read_text())

    def test_multi_region_splice_independence(self):
        entries = [{"category": "Cat New", "tags": ["tag-new"]}]
        fx = SyncFixture(self.tmpdir, entries, schema_categories=["Cat A"],
                          template_categories=["Cat A"], template_tags=["tag-a"])
        result = fx.run("--write")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        text = fx.template_a.read_text()
        # both blocks must have updated correctly, and the file must still be
        # well-formed (markers present, no corruption from index drift).
        self.assertIn("- Cat New", text)
        self.assertIn("- label: tag-new", text)
        self.assertEqual(text.count("BEGIN AUTO-GENERATED CATEGORIES"), 1)
        self.assertEqual(text.count("BEGIN AUTO-GENERATED TAGS"), 1)
        self.assertEqual(text.count("END AUTO-GENERATED CATEGORIES"), 1)
        self.assertEqual(text.count("END AUTO-GENERATED TAGS"), 1)

    def test_missing_markers_errors_cleanly(self):
        entries = [{"category": "Cat A", "tags": ["tag-a"]}]
        fx = SyncFixture(self.tmpdir, entries, schema_categories=["Cat A"])
        fx.template_a.write_text(TEMPLATE_NO_MARKERS, encoding="utf-8")
        result = fx.run("--check")
        self.assertEqual(result.returncode, 2)
        self.assertIn("marker", result.stderr)

    def test_write_is_idempotent(self):
        entries = [{"category": "Cat A", "tags": ["tag-a", "tag-b"]}]
        fx = SyncFixture(self.tmpdir, entries, schema_categories=["Cat A"],
                          template_tags=["tag-a"])
        first = fx.run("--write")
        self.assertEqual(first.returncode, 0)
        second = fx.run("--write")
        self.assertEqual(second.returncode, 0)
        self.assertIn("Already in sync", second.stdout)


if __name__ == "__main__":
    unittest.main()
