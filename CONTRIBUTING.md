# Contributing

This repo is a gallery of community Lua Apps and Widgets for EdgeTX. [`scripts.json`](scripts.json) is the
single source of content — entries are validated against [`scripts.schema.json`](scripts.schema.json) and
rendered into the [gallery site](https://edgetx.org/lua-scripts/).

## Submitting or updating a gallery entry

You don't need to edit `scripts.json` yourself — open an issue instead:

- [Add a Lua App or Widget to the Gallery](https://github.com/EdgeTX/lua-scripts/issues/new?template=add-script.yml)
- [Update / Correct a Lua App or Widget Entry](https://github.com/EdgeTX/lua-scripts/issues/new?template=update-script.yml)
- [Feedback / Report an Issue](https://github.com/EdgeTX/lua-scripts/issues/new?template=feedback.yml)

Fill in the form fields — name, category, description, info URL, and (optionally) screenshots. Screenshot URLs
can be external links (raw GitHub, Imgur, etc.) or you can drag-and-drop / paste image files directly into the
form and GitHub will host them for you.

## What happens after you submit

1. A maintainer reviews the issue and applies the `add-to-gallery` (new entry) or `update-in-gallery`
   (existing entry) label.
2. That label triggers [`script-submission.yml`](.github/workflows/script-submission.yml), which parses the
   issue, updates `scripts.json`, validates it, and opens a **draft PR** back to the issue.
3. If the submission included external image URLs, a maintainer applies the `localize-images` label to the
   draft PR. This triggers [`localize-images.yml`](.github/workflows/localize-images.yml), which downloads
   those images into `ASSETS/<slug>/`, rewrites `scripts.json` to point at the local copies, and pushes the
   result back to the PR branch as a commit.
4. Once the diff looks correct, a maintainer removes draft status and merges.
5. Merging to `main` regenerates the gallery site via [`gh-pages.yml`](.github/workflows/gh-pages.yml).

## CI checks

- [`validate-scripts-json.yml`](.github/workflows/validate-scripts-json.yml) validates `scripts.json` against
  `scripts.schema.json` on every push/PR that touches it.
- [`validate-issue-templates.yml`](.github/workflows/validate-issue-templates.yml) keeps the tag/category
  dropdowns in the issue templates in sync with `scripts.schema.json`, and self-heals same-repo branches
  automatically when they drift.

## AI tools

An AI collaboration guide is maintained at [`.ai/instructions.md`](.ai/instructions.md). It is symlinked from
`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.cursorrules`, `.windsurfrules`, and `.github/copilot-instructions.md`
so all common AI/LLM tools pick it up automatically. Update it when repo-specific workflows change or when you
find yourself correcting an AI agent on the same point twice.

## Running the tooling locally

The scripts under [`tools/`](tools/) are plain Python, run via [`uv`](https://docs.astral.sh/uv/) — no project
setup required beyond having `uv` installed:

```bash
uv run tools/validate_scripts.py --scripts-json scripts.json
uv run tools/download_external_images.py --dry-run   # preview image localization
uv run tools/sync_issue_template_options.py --check   # check tag/category drift
```
