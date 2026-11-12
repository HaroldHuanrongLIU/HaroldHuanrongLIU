# Maintaining the profile

Edit `profile.json` for personal fields. Blank entries separate groups. The ASCII portrait is the approved v3 sampling of the account's GitHub avatar, stored in `assets/avatar.json`; routine refreshes never replace it.

Generate using Python 3.9 or newer, with no third-party packages:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/update_profile.py
```

`GITHUB_TOKEN` is optional locally. It increases the REST API allowance when set and is supplied automatically in Actions. No personal token or external image service is needed. Credentials are sent only to `api.github.com`, not the public contribution page.

To reproduce a saved snapshot without network access:

```sh
python3 scripts/update_profile.py --offline
```

The source inputs are `profile.json`, `assets/avatar.json`, and live GitHub data. The generated outputs are `assets/profile-dark.svg`, `assets/profile-light.svg`, their `-mobile.svg` variants, and `assets/github-stats.json`. The README selects a stacked card below a 600px viewport so the text stays readable. Do not edit the SVGs by hand.

## Statistics

- **Uptime:** calendar age of the GitHub account, calculated in Asia/Shanghai; month-end anniversaries clamp to the last day of the month.
- **Repos:** owned public non-Fork repositories, including archived repositories.
- **Forks:** owned public Fork repositories, shown separately.
- **Stars:** stars received by the non-Fork repositories only, not repositories this account has starred.
- **Contributions.1y:** the total displayed by the anonymous public GitHub contribution calendar. This can include anonymized private contribution counts if the account owner chooses to publish them. It is not a lifetime commit count.
- **Snapshot:** the collection time in UTC+8. README image caches can delay its appearance.

The account and repository counts use the [public REST API](https://docs.github.com/en/rest/repos/repos#list-repositories-for-a-user), including every repository page. The contribution total is read from the public `https://github.com/users/HaroldHuanrongLIU/contributions` heading. That HTML is not a versioned API: if GitHub changes it, the job fails visibly and retains the previous published assets, rather than substituting zero.

## Automatic updates

The workflow runs every six hours at minute 17, on changes to generation inputs on `main`, or via **Actions → Update profile → Run workflow**. Publication is enabled only on `main`; manual runs on another branch exercise generation without publishing. The workflow must be pushed to the default branch before scheduling is active.

The built-in token needs `contents: write` to publish generated assets. A repository rule that prohibits bot commits can prevent publication; check the job log rather than assuming a refreshed card was published. A concurrent upstream push causes a safe non-fast-forward failure; rerun on the latest main. No force-push or automatic rebase is used.

Tests and all data fetching/rendering must succeed before the publish step. Only the five generated files are staged. The last successful card and its timestamp remain visible after a failed job. Scheduled runs can be delayed, and GitHub can disable schedules in inactive public repositories after 60 days; see [GitHub scheduling behavior](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule).

Visual reference: [Andrew6rant's Neofetch-style profile](https://github.com/Andrew6rant). The content and avatar belong to this profile.
