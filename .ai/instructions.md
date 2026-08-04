# EdgeTX Lua Scripts Gallery — AI Collaboration Guide

This document provides context for AI coding assistants (Claude Code, Copilot, Cursor, Gemini, Windsurf, etc.)
working in this repository.

## What this repo is

This is **not** a repo of Lua source code. It's a community-maintained gallery/index of *links* to EdgeTX Lua
Apps and Widgets hosted elsewhere. The actual Lua scripts live in their authors' own repos; this repo just
catalogs them (name, category, description, link, screenshots, tags) and renders that catalog into a static
website. There is no Lua code to write, build, or run here — the "codebase" is a JSON data file, a JSON
schema, some Python tooling, and GitHub Actions automation that together turn issue-form submissions into
gallery entries.

## Canonical data

`scripts.json` is the single source of truth — an array of entries validated against `scripts.schema.json`.
Each entry: `name`, `category`, `description`, `infourl` (must start with `http://`/`https://`), `images`
(local `ASSETS/<slug>/...` paths and/or external URLs), `tags` (non-empty list).

`scripts.schema.json` also doubles as the canonical vocabulary for `category` and `tags` — its
`items.properties.category.examples` and `items.properties.tags.items.examples` arrays are machine-generated
(see below) and must never be hand-edited.

Humans normally never touch `scripts.json` directly — new/updated entries come in through GitHub Issue Forms
and get applied by CI (see Pipeline below). Direct edits are fine for maintenance (fixing a broken link,
renaming a category, etc.) but must go through `tools/validate_scripts.py` and keep
`tools/sync_issue_template_options.py --check` clean afterward.

## Commands

All tooling is dependency-free stdlib Python, run via `uv` (no `pyproject.toml`/install step needed):

```bash
# Validate scripts.json against required fields / URL format / duplicate names
uv run tools/validate_scripts.py --scripts-json scripts.json

# Check (or fix) drift between scripts.json usage and the schema examples /
# issue-form dropdown+checkbox blocks
uv run tools/sync_issue_template_options.py --check
uv run tools/sync_issue_template_options.py --write
uv run tools/sync_issue_template_options.py --write --prune-categories   # also drop unused categories

# Run the sync script's own unit tests
uv run tools/test_sync_issue_template_options.py

# Preview / perform localizing external image URLs into ASSETS/<slug>/
uv run tools/download_external_images.py --dry-run
uv run tools/download_external_images.py
uv run tools/download_external_images.py --name "Some App"   # single entry

# Parse a GitHub Issue Form body into a scripts.json entry (used by CI, rarely run manually)
uv run tools/issue_to_scripts.py --issue-body <path> --scripts-json scripts.json --mode insert
uv run tools/issue_to_scripts.py --issue-body <path> --scripts-json scripts.json --mode patch

# Regenerate the static gallery site (Tailwind + Alpine.js, self-contained index.html)
uv run tools/generate_site.py --scripts-json scripts.json --assets-dir ASSETS --output-dir site
```

Run a single test from `test_sync_issue_template_options.py` with standard `unittest` selection:
```bash
uv run tools/test_sync_issue_template_options.py TestSync.test_write_is_idempotent
```

## Architecture: the submission pipeline

This is the part that requires reading multiple files together to understand. End-to-end flow from a
contributor's issue to a live gallery entry:

1. **Issue Forms** (`.github/ISSUE_TEMPLATE/add-script.yml`, `update-script.yml`) collect App Name, Category
   (dropdown, or free-text "New Category"), Description, Info URL, Image URLs (external links, or
   drag/paste which GitHub auto-hosts), and Tags (checkboxes + free-text "Additional Tags"). The Category
   dropdown and Tags checkboxes each live inside `# --- BEGIN/END AUTO-GENERATED ... ---` marker comments —
   don't hand-edit the values inside those blocks, they're regenerated (see step 5).

2. **Maintainer applies a label** (`add-to-gallery` or `update-in-gallery`) to the issue. This triggers
   `.github/workflows/script-submission.yml`, which:
   - writes the issue body to a temp file and runs `tools/issue_to_scripts.py` (mode `insert` for
     `add-to-gallery`, `patch` for `update-in-gallery`) to update `scripts.json` in place
   - runs `tools/validate_scripts.py`
   - runs `tools/sync_issue_template_options.py --write` to refresh schema/template vocab
   - commits to a new branch `add-script/<issue-number>` and opens a **draft PR** back to the issue, with a
     checklist for the maintainer

3. **Optional image localization**: if the draft PR still has external image URLs, applying the
   `localize-images` label triggers `.github/workflows/localize-images.yml`, which runs
   `tools/download_external_images.py` (downloads into `ASSETS/<slug>/`, rewrites `scripts.json` to local
   paths) and pushes a follow-up commit to the same PR branch. This only works for same-repo branches —
   `GITHUB_TOKEN` can't push to a fork.

4. **Merge to `main`** triggers `.github/workflows/gh-pages.yml`, which runs `tools/generate_site.py` and
   deploys `site/` to GitHub Pages (https://edgetx.org/lua-scripts/). The same workflow also builds a preview
   artifact on PRs touching `ASSETS/**`, `scripts.json`, or the generator itself.

5. **Vocabulary sync** is enforced continuously by `.github/workflows/validate-issue-templates.yml`, driven
   by `tools/sync_issue_template_options.py`:
   - **tags** are a pure snapshot of current usage in `scripts.json` — a tag that stops being used drops out
     on the next `--write`
   - **categories** are monotonic add-only by default (a category doesn't disappear from the dropdown just
     because it's briefly at zero entries, since categories drive the site's top-level nav tabs);
     `--prune-categories` deliberately overrides that
   - on `push`, the `sync` job self-heals same-repo branches by committing corrections directly (safe: a
     `GITHUB_TOKEN`-authored push doesn't retrigger workflows)
   - on `pull_request`, a read-only `check` job just fails if out of sync
   - on `pull_request_target` from a **fork**, `suggest-fix-for-fork-prs` computes the same fix against the
     fork's `scripts.json` (fetched as inert data, never executed) but can only post it as a sticky PR
     comment, since `GITHUB_TOKEN` can't push to fork branches

6. **`validate-scripts-json.yml`** independently re-validates `scripts.json` on any push/PR touching it, as a
   backstop outside the label-triggered flow (e.g. direct maintainer edits).

When changing `tools/sync_issue_template_options.py` behavior, keep `tools/test_sync_issue_template_options.py`
in sync — it's a real regression suite (idempotency, marker-splice independence, monotonic-category-removal
semantics, etc.), and `validate-issue-templates.yml` runs it before every `--check`/`--write`.

## Conventions

- Commit messages in this repo follow `type(scope): subject` (see `git log`), e.g.
  `feat(scripts): Add script <name>`, `feat(ci): ...`, `fix(ci): ...`.
- `ASSETS/<slug>/` directories hold local screenshots per entry; `entry_slug()` in
  `download_external_images.py` derives the slug from an entry's existing `ASSETS/` path if one exists
  (so a renamed entry doesn't get split across two directories), falling back to slugifying the name.
- Category/tag "examples" arrays in `scripts.schema.json` are sorted case-insensitively (`str.casefold`) —
  preserve that ordering; the sync `--check` treats an out-of-order-but-same-set list as drift, not just a
  set-difference.
