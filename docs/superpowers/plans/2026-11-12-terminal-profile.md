# Terminal Profile Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver the approved profile README with automatic public GitHub snapshots.

**Architecture:** A standard-library Python script reads profile configuration and the preserved v3 avatar, collects public GitHub metadata, and writes light/dark SVGs plus a snapshot. GitHub Actions validates, regenerates, and commits only these generated assets.

**Tech Stack:** Python 3.9-compatible standard library; Python 3.12 in GitHub Actions; SVG, JSON, Markdown.

**Spec:** `docs/superpowers/specs/2026-11-12-terminal-profile-design.md`

## Global Constraints

- Preserve approved v3 avatar samples and all approved field values, including GPT and ENG.
- Public non-Fork repositories own the Repos and Stars metrics; Forks is separate.
- Keep previous published artifacts on a failed refresh; no invented or default-zero statistics.
- Reuse the current checkout on feat/terminal-profile. The user explicitly authorized committing all changes and pushing to main on 2026-11-12.
- User approved execution; proceed inline without repeating the design approval gate.

## Review Focus

- More than 100 repositories must not truncate the count: test a second page.
- Large Fork star counts must not inflate original project stars: synthetic Fork fixture.
- A changed/sign-in contribution page must fail without replacing existing assets: missing-header and failed-refresh tests.
- GitHub token must not be included in requests to public HTML: transport-boundary test.
- Month ends and XML-sensitive field values must remain valid: date and parsed-SVG tests.

### Task 1: Generator and data contracts

**Files:** `scripts/update_profile.py`, `tests/test_update_profile.py`, `profile.json`, `assets/avatar.json`.
**Interfaces:** `account_age(created: date, today: date) -> str`; `parse_contributions(html: str) -> int`; `collect_stats(username: str, now: datetime, token: str) -> dict`; `render_card(profile: dict, avatar: dict, stats: dict, theme: str) -> str`; `update(root: Path, offline: bool = False) -> dict`.

- [x] Write boundary tests for age, contribution parsing, paginated metrics, token routing, valid SVG and failure preservation.
- [x] Run `python3 -m unittest discover -s tests -v`; observe missing implementation failure.
- [x] Implement the generator with optional offline regeneration, and extract the exact approved v3 avatar data.
- [x] Run the complete suite; all tests pass.

### Task 2: README and scheduled delivery

**Files:** `README.md`, `.github/workflows/update-profile.yml`, `.github/PROFILE.md`, `assets/profile-dark.svg`, `assets/profile-light.svg`, `assets/github-stats.json`.
**Interfaces:** workflow calls `python scripts/update_profile.py`; README embeds generated variants.

- [x] Replace the biography with an accessible picture and working native links.
- [x] Configure cron `17 */6 * * *`, manual dispatch and main input-path changes; scoped staging, concurrency, timeout and contents write permission.
- [x] Generate using live public endpoints; verify both SVGs and snapshot agree.
- [x] Run offline generation and ensure it reproduces the existing outputs.
- [x] Inspect browser rendering in light/dark and at a narrow width; validate workflow configuration and the complete diff.

### Task 3: Final review and delivery

- [x] Fresh read-only review of generator, statistics, workflow and approved design.
- [x] Fix material findings and run affected checks; no material findings remained.
- [x] Report local deliverables and validation and obtain publication approval.
- [ ] Publish to main and confirm the first GitHub Actions refresh and asset commit succeed.

## Execution notes

- Live collection succeeded with 7 non-Fork repos, 356 Forks, 5 stars, 19 followers and 2,741 contributions.
- The initial six tests failed before implementation and passed afterward. Independent review found no material issue.
- Ruling: add light/dark mobile variants after browser QA showed that a single desktop image made phone text too small. A new mobile test failed first, then passed with the implementation. All five outputs are explicitly staged by the workflow.
- Publication approval received: commit all changes, push to main, and confirm the first automatic update succeeds.
- Final verification: seven unit tests pass; all four SVGs parse; all five generated artifacts reproduce byte-for-byte offline; YAML schedule/dispatch/permissions checks pass; desktop and mobile picture selection verified without horizontal overflow. Independent review of the original implementation and mobile delta found no material issues. GitHub-hosted execution is pending publication approval.
