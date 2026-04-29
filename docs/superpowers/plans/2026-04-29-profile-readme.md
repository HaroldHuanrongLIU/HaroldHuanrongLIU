# Profile README Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a clean English GitHub Profile README that introduces Harold Huanrong LIU as an academic researcher and highlights OmniUp plus restrained GitHub activity.

**Architecture:** This is a single-file Markdown profile project. `README.md` owns all public-facing content, external links, selected publications, recent highlights, and lightweight GitHub stats cards. The existing `.gitignore` keeps local brainstorming and browser inspection artifacts out of version control.

**Tech Stack:** GitHub-flavored Markdown, GitHub Profile README rendering, Git, and GitHub Readme Stats image endpoints documented through Context7 as `/anuraghazra/github-readme-stats`.

---

## File Structure

- Create: `README.md` - the GitHub Profile README shown on the profile repository.
- Use existing: `.gitignore` - already excludes `.superpowers/`, `.playwright-mcp/`, `.DS_Store`, and the temporary visual companion screenshot.
- Use existing: `docs/superpowers/specs/2026-04-29-profile-readme-design.md` - source design spec.

## Task 1: Create The README

**Files:**
- Create: `README.md`

- [ ] **Step 1: Confirm README baseline**

Run:

```bash
test -f README.md
```

Expected: command exits non-zero because `README.md` does not exist yet.

- [ ] **Step 2: Add the Profile README content**

Create `README.md` with exactly this content:

```markdown
# Hi, I'm Harold Huanrong LIU

I am currently a second-year MSc student in [Artificial Intelligence](https://www.cis.um.edu.mo/msc_artificial_intelligence.html) and an incoming PhD student in [Computer and Information Science](https://www.cis.um.edu.mo) at the [University of Macau](https://um.edu.mo), advised by [Prof. Qingbiao LI](https://www.fst.um.edu.mo/people/qingbiaoli/). My work focuses on surgical robotics, medical image analysis, surgical trajectory prediction, and efficient machine learning systems.

[Website](https://haroldhuanrongliu.github.io/) · [Google Scholar](https://scholar.google.com/citations?user=9LK8IdYAAAAJ&hl=en) · [GitHub](https://github.com/HaroldHuanrongLIU) · [OmniUp](https://github.com/HaroldHuanrongLIU/Omniup) · [Contact](https://haroldhuanrongliu.github.io/)

## Research

- **Surgical robotics:** Learning and evaluating trajectories for autonomous surgical systems.
- **Medical image analysis:** Vision models for surgical understanding and decision support.
- **Efficient ML systems:** Runtime pruning, low-rank adaptation, and query-adaptive quantization for efficient model inference.

## Featured Project

**[OmniUp](https://github.com/HaroldHuanrongLIU/Omniup)** is an open-source project I maintain on GitHub. It is the main project I highlight here; the full project context lives in the repository.

## Selected Publications

- **SutureAgent: Learning Surgical Trajectories via Goal-conditioned Offline RL in Pixel Space**. arXiv preprint, submitted to MICCAI 2026. [arXiv](https://arxiv.org/abs/2603.26720) · [PDF](https://arxiv.org/pdf/2603.26720)
- **Runtime Adaptive Pruning for LLM Inference**. arXiv preprint, submitted to ICML 2026. [arXiv](https://arxiv.org/abs/2505.17138) · [PDF](https://arxiv.org/pdf/2505.17138) · [OpenReview](https://openreview.net/forum?id=2f9RPk7MQe)
- **Less is More: Resource-Efficient Low-Rank Adaptation**. arXiv preprint, submitted to ACL 2026. [arXiv](https://arxiv.org/abs/2512.00878) · [PDF](https://www.arxiv.org/pdf/2512.00878) · [OpenReview](https://openreview.net/forum?id=8XvvF3yxP7)
- **QAQ: Query-adaptive Mixed-precision Quantization for Large Language Models**. NeurIPS 2025 Workshop on Machine Learning for Systems. [OpenReview](https://openreview.net/forum?id=dpHfDasG44) · [NeurIPS](https://neurips.cc/virtual/2025/loc/san-diego/129098)

See the [personal website](https://haroldhuanrongliu.github.io/) for the complete publication list and BibTeX entries.

## Recent Highlights

- **2026.04:** [OmniUp](https://github.com/HaroldHuanrongLIU/Omniup) is available as an open-source project on GitHub.
- **2026.03:** SutureAgent is available on [arXiv](https://arxiv.org/abs/2603.26720).
- **2025.12:** Received UM PhD Teaching Research Assistant - Type A.

## GitHub Snapshot

The cards below are a lightweight snapshot; the profile remains readable without them.

<p>
  <img height="165" alt="Harold Huanrong LIU GitHub stats" src="https://github-readme-stats.vercel.app/api?username=HaroldHuanrongLIU&show_icons=true&hide_border=true" />
  <img height="165" alt="Harold Huanrong LIU top languages" src="https://github-readme-stats.vercel.app/api/top-langs/?username=HaroldHuanrongLIU&hide_border=true" />
</p>

## More Information

For the full CV-style view, including education, awards, research experience, teaching, and publication details, visit [haroldhuanrongliu.github.io](https://haroldhuanrongliu.github.io/).
```

- [ ] **Step 3: Verify the section outline**

Run:

```bash
rg -n "^(#|##) " README.md
```

Expected output:

```text
1:# Hi, I'm Harold Huanrong LIU
7:## Research
13:## Featured Project
17:## Selected Publications
26:## Recent Highlights
32:## GitHub Snapshot
41:## More Information
```

- [ ] **Step 4: Inspect the Markdown source**

Run:

```bash
sed -n '1,120p' README.md
```

Expected: the full README source prints once, with no direct email address, no local image paths, and no broken Markdown list indentation.

## Task 2: Verify Links, Fallbacks, And Repository Hygiene

**Files:**
- Modify: `README.md` only if verification exposes a typo.

- [ ] **Step 1: Confirm there is no direct email exposure**

Run:

```bash
rg -n "mailto:|@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}" README.md
```

Expected: no output and exit code `1`.

- [ ] **Step 2: Confirm GitHub stats endpoints match the documented API shape**

Run:

```bash
rg -n "github-readme-stats.vercel.app/api" README.md
```

Expected output:

```text
37:  <img height="165" alt="Harold Huanrong LIU GitHub stats" src="https://github-readme-stats.vercel.app/api?username=HaroldHuanrongLIU&show_icons=true&hide_border=true" />
38:  <img height="165" alt="Harold Huanrong LIU top languages" src="https://github-readme-stats.vercel.app/api/top-langs/?username=HaroldHuanrongLIU&hide_border=true" />
```

- [ ] **Step 3: Verify core public links**

Run these commands:

```bash
curl -I -L https://haroldhuanrongliu.github.io/
curl -I -L https://github.com/HaroldHuanrongLIU/Omniup
curl -I -L https://arxiv.org/abs/2603.26720
curl -I -L https://openreview.net/forum?id=2f9RPk7MQe
```

Expected: each command reaches a successful final response such as `HTTP/2 200`, `HTTP/1.1 200`, or a redirect chain ending in a successful response.

- [ ] **Step 4: Confirm local artifacts are ignored**

Run:

```bash
git check-ignore .superpowers/ .playwright-mcp/ profile-readme-directions.png
```

Expected output:

```text
.superpowers/
.playwright-mcp/
profile-readme-directions.png
```

- [ ] **Step 5: Commit the README**

Run:

```bash
git add README.md
git commit -m "Add hybrid GitHub profile README"
```

Expected: git creates a commit containing only `README.md`.

## Task 3: Final Verification

**Files:**
- Inspect: repository state only.

- [ ] **Step 1: Confirm working tree is clean**

Run:

```bash
git status --short
```

Expected: no output.

- [ ] **Step 2: Confirm recent commit history**

Run:

```bash
git log --oneline -2
```

Expected: output includes these two commits, newest first:

```text
<new-sha> Add hybrid GitHub profile README
7472665 Add profile README design spec
```
