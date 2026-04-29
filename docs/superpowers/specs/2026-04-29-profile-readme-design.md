# Profile README Design

## Purpose

Create a GitHub Profile README for Harold Huanrong LIU that acts as both an academic homepage entry point and a restrained open-source showcase. The README should quickly communicate Harold's research identity, direct visitors to the full personal website, and highlight selected GitHub work without turning into a badge-heavy developer profile.

## Source Material

Primary content should be adapted from `https://haroldhuanrongliu.github.io/`, including:

- Biography: MSc student in Artificial Intelligence and incoming PhD student in Computer and Information Science at University of Macau.
- Research direction: surgical robotics, medical image analysis, surgical trajectory prediction, autonomous surgical robotics, and efficient machine learning systems.
- Featured open-source project: OmniUp.
- Selected publications: SutureAgent, Runtime Adaptive Pruning for LLM Inference, Less is More: Resource-Efficient Low-Rank Adaptation, and QAQ.
- Recent highlights: OmniUp open-source release, SutureAgent arXiv availability, and UM PhD Teaching Research Assistant - Type A.
- External links: personal website, Google Scholar, DBLP, ORCID, Semantic Scholar, ResearchGate, X, GitHub, and non-direct contact through the website.

## Direction

Use the approved Hybrid Academic + Open Source direction.

The README should place academic identity first, then give OmniUp and GitHub activity meaningful but secondary visibility. It should feel suitable for international academic visitors and GitHub visitors who want to understand what Harold works on and where to find more details.

## Content Structure

The README should contain these sections in order:

1. Hero intro: name, current identity, research focus, and quick links to Website, Google Scholar, GitHub, and OmniUp.
2. Research: 2-3 concise bullets covering surgical robotics, medical image analysis, surgical trajectory prediction, and efficient ML systems.
3. Featured Project: a compact OmniUp section with one-sentence positioning and a repository link.
4. Selected Publications: 3-4 representative publications with title, status or venue, year, and links when available.
5. GitHub Snapshot: restrained GitHub stats and top-languages cards.
6. Recent Highlights: 2-3 short homepage-derived updates.
7. More Information: link to the personal homepage for full CV, publications, experience, education, awards, and teaching details.

## Style

The README should be fully in English. The writing should be concise, professional, and academic, with GitHub-native formatting. Avoid heavy animations, trophy walls, visitor counters, oversized badge stacks, and noisy decorative elements.

Preferred tone:

- Clear and direct.
- Research-focused.
- Polished but not promotional.
- Short enough to scan from the GitHub profile page.

## Implementation Shape

Create the project from the currently empty directory using:

- `README.md` as the main GitHub Profile README.
- A minimal `.gitignore` that excludes brainstorming and local inspection artifacts.
- Optional `assets/` only if a local avatar or image is intentionally added later.

The README should not depend on local assets unless those assets are committed. If GitHub stats cards are used, the core identity, links, and project descriptions must remain useful even if those external cards fail to load.

## Data And Links

Use public links from the homepage and keep them explicit in Markdown. Do not expose a direct email address in the initial Profile README; use the personal website as the contact path unless Harold explicitly asks to add a `mailto:` link later.

Publication entries should remain compact and should not reproduce full BibTeX or long author lists. The personal website remains the canonical place for complete publication details.

## Error Handling And Maintenance

The README should degrade gracefully:

- No critical information should appear only inside generated SVG stat cards.
- Broken or unavailable external stat services should not make the README look empty.
- Relative image paths should be avoided unless the files are present in the repository.
- The homepage should be used as the canonical source for detailed and frequently updated academic information.

## Verification

Before considering implementation complete:

- Inspect `README.md` as Markdown source for readability.
- Verify all public links used in the README.
- Confirm no temporary `.superpowers/` or Playwright artifacts are tracked.
- Confirm GitHub stat image URLs are optional visual support, not the only source of key information.
