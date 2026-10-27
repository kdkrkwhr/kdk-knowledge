# Personal Knowledge Hub Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a source pinned personal knowledge hub foundation.

**Architecture:** Static Pages assets read a small curated JSON graph. A Python standard library validator enforces public evidence and site boundaries; CI deploys the checked site.

**Tech Stack:** HTML, CSS, JavaScript, JSON, Python standard library, GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-10-27-personal-knowledge-hub-design.md`

## Global Constraints

- Do not run Graphify or contact an LLM API.
- Do not publish unverified private history, outcomes, or personal data.
- Do not change the referenced repositories.

## Review Focus

- A relation without valid public pinned evidence must fail validation.
- Empty search/filter results must be explained.
- A mobile viewport must avoid horizontal page overflow.
- Curated relations must never be labeled Graphify extraction.
- A broken source URL or missing revision must fail validation.

---

### Task 1: Evidence and validation

**Files:** `site/knowledge.json`, `scripts/validate.py`, `tests/test_validate.py`

**Interfaces:** validator `validate(root: Path) -> list[str]` checks JSON references and public site files; returns errors.

- [ ] Write failing tests for pinned public evidence and relation reference checks.
- [ ] Run `python3 -m unittest discover -s tests -v` and see expected failures.
- [ ] Implement the dataset and validator.
- [ ] Run the suite and see zero failures.

### Task 2: Human wiki and curated map

**Files:** `site/index.html`, `site/architecture/index.html`, `site/style.css`, `site/wiki.js`, `site/architecture/map.js`, `templates/*.md`, `README.md`

**Interfaces:** both pages link source IDs and separate reviewed prose from curated relations; the map reads `../knowledge.json`.

- [ ] Add static content and interaction checks for navigation, empty results, and labels.
- [ ] Run tests, then implement pages and scripts.
- [ ] Run tests and inspect desktop and mobile browser screenshots.

### Task 3: CI and publication

**Files:** `.github/workflows/pages.yml`

- [ ] Add a CI workflow that validates and uploads only `site/`.
- [ ] Run validation and the full test suite; inspect staged files.
- [ ] Commit and push to `main`; verify remote SHA and CI.
- [ ] Check Pages state and the public URL.
