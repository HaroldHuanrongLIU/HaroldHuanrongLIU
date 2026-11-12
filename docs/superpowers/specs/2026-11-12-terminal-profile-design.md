# Approved terminal profile

The user approved the filled Neofetch-style preview and explicitly requested README implementation and automatic GitHub updates on 2026-11-12.

## Intent and scope

Replace the existing biography with a compact two-column profile modeled on Andrew6rant's layout: approved v3 ASCII portrait on the left, dense monospace fields with dotted leaders on the right, orange keys and blue values, and matching light/dark variants. Use the approved v3 96 × 70 samples, crop (78, 20, 304, 440), not the later sharpened v4.

The existing Markdown research sections are intentionally replaced. No website, browser terminal, AI API, or new personal contact details are required. The user authorized committing all changes, pushing to main, and verifying the first automatic update on 2026-11-12.

## Approaches

- Selected: generated SVGs embedded in the GitHub profile README, refreshed by GitHub Actions. Keeps the profile readable without a running image service.
- Rejected: multi-pane tmux dashboard, because the user selected the simpler single-card approach.
- Rejected: independent interactive terminal website, because the requested destination is the README.

## Approved content

Header: `harold@liu`; account: `HaroldHuanrongLIU`.

| Field | Value |
| --- | --- |
| OS | macOS |
| Host | University of Macau |
| Kernel | PhD Student |
| IDE | Codex |
| Languages.Programming | GPT |
| Languages.Computer | LaTeX, Markdown, HTML |
| Languages.Real | ENG |
| Hobbies.Software | Apple |
| Hobbies.Hardware | MacBook |
| Website | huanrongliu.com |

Omit email and Discord. Uptime is GitHub account age, not personal age. Website and GitHub must remain reachable links.

## Data and update contract

- Repos counts owned public non-Fork repositories; Forks is separate.
- Stars sums only those non-Fork repositories; Followers comes from the public account.
- Contributions.1y is the total shown on the public GitHub contribution calendar, including any anonymized contribution count the user publishes there.
- Snapshot time uses Asia/Shanghai (UTC+8). Display genuine snapshot timestamps, not a simulated live status.
- Run every six hours, on relevant input changes on main, and on manual dispatch.
- Collect all required data and render both variants before writing outputs. An HTTP error or unexpected contribution markup must fail the run and retain the last published card.
- Use the workflow's GITHUB_TOKEN for REST requests and repository writes; no personal token is required. Do not send it to the public HTML endpoint.

## Builder decisions

Use Python standard library, JSON inputs, generated SVGs and a reproducible stats snapshot. The public contribution HTML endpoint is used so the count matches the reviewed public profile without a personal GraphQL token. Unexpected markup is an explicit failure, never a zero count. Publish after local verification under the user's explicit authorization.

Browser verification found that scaling the desktop SVG made mobile text unreadable. Preserve the approved preview's narrow layout with separate 420px stacked light/dark variants selected by picture media queries below 600px. This changes delivery geometry only; the v3 portrait samples and content stay the same.

## Acceptance

Verify pagination and Fork accounting, month-end and leap-day age calculations, missing contribution data, preservation on network failure, valid escaped SVG, both color modes, narrow README display, and input-to-output regeneration. Review the complete local diff before delivery.
