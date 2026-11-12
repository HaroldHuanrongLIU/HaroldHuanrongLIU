"""Render the approved profile using public GitHub data and the fixed v3 portrait."""

import argparse
import calendar
import json
import math
import os
import re
from datetime import date, datetime, timezone
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


LOCAL_TIME = ZoneInfo("Asia/Shanghai")
ROOT = Path(__file__).resolve().parents[1]
PALETTES = {
    "dark": {"background": "#161b22", "ink": "#c9d1d9", "key": "#ffa657",
             "value": "#a5d6ff", "dots": "#616e7f"},
    "light": {"background": "#f6f8fa", "ink": "#24292f", "key": "#953800",
              "value": "#0a3069", "dots": "#c2cfde"},
}


def account_age(created: date, today: date) -> str:
    months = (today.year - created.year) * 12 + today.month - created.month

    def anniversary(offset):
        year, month = divmod(created.year * 12 + created.month - 1 + offset, 12)
        month += 1
        return date(year, month, min(created.day, calendar.monthrange(year, month)[1]))

    if anniversary(months) > today:
        months -= 1
    years, months_left = divmod(months, 12)
    days = (today - anniversary(months)).days
    return ", ".join(f"{value} {unit}{'' if value == 1 else 's'}"
                     for value, unit in ((years, "year"), (months_left, "month"), (days, "day")))


class ContributionHeadings(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_heading = False
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag == "h2":
            self.in_heading = True

    def handle_endtag(self, tag):
        if tag == "h2":
            self.in_heading = False

    def handle_data(self, data):
        if self.in_heading:
            self.parts.append(data)


def parse_contributions(html: str) -> int:
    headings = ContributionHeadings()
    headings.feed(html)
    match = re.search(r"([0-9][0-9,]*)\s+contributions?\s+in the last year",
                      " ".join(headings.parts))
    if not match:
        raise ValueError("GitHub contribution total is missing; keeping the previous snapshot")
    return int(match.group(1).replace(",", ""))


def fetch(url: str, token: str = "") -> str:
    headers = {"User-Agent": "HaroldHuanrongLIU-profile-update", "Accept-Language": "en-US"}
    if url.startswith("https://api.github.com/"):
        headers.update({"Accept": "application/vnd.github+json",
                        "X-GitHub-Api-Version": "2026-03-10"})
        if token:
            headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request(url, headers=headers), timeout=30) as response:
        return response.read().decode("utf-8")


def collect_stats(username: str, now: datetime, token: str = "") -> dict:
    user_path = quote(username, safe="")
    api = f"https://api.github.com/users/{user_path}"
    user = json.loads(fetch(api, token))
    repositories = []
    page = 1
    while True:
        batch = json.loads(fetch(f"{api}/repos?type=owner&per_page=100&page={page}", token))
        repositories.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    originals = [repo for repo in repositories if not repo["fork"]]
    contributions = parse_contributions(fetch(
        f"https://github.com/users/{user_path}/contributions"))
    return {
        "username": username,
        "created_at": user["created_at"],
        "repos": len(originals),
        "forks": len(repositories) - len(originals),
        "stars": sum(repo["stargazers_count"] for repo in originals),
        "followers": user["followers"],
        "contributions": contributions,
        "as_of": now.astimezone(timezone.utc).isoformat(timespec="seconds"),
    }


def render_avatar(avatar: dict, dark: bool) -> str:
    cols, rows, rgb = avatar["cols"], avatar["rows"], avatar["rgb"]
    if cols <= 0 or rows <= 0 or len(rgb) != cols * rows * 3:
        raise ValueError("Invalid avatar dimensions or RGB sample count")
    size = 365 / (cols * 0.6)
    ramp = " .:-=+*#%@"
    output = [f'<g aria-hidden="true" font-size="{size:.6f}" font-weight="700">']
    for y in range(rows):
        spans = []
        for x in range(cols):
            i = (y * cols + x) * 3
            luminance = (.2126 * rgb[i] + .7152 * rgb[i + 1] + .0722 * rgb[i + 2]) / 255
            tone = max(0, min(1, (luminance - .10) / .78))
            # Math.floor(x + .5) matches the approved JavaScript preview's rounding.
            character = ramp[math.floor(math.sqrt(tone if dark else 1 - tone) * 9 + .5)]
            shade = math.floor((120 + 135 * tone if dark else 125 * tone) + .5)
            spans.append(f'<tspan fill="#{shade:02x}{shade:02x}{shade:02x}">{character}</tspan>')
        baseline = 15 + size + y * size * 1.2
        output.append(f'<text x="15" y="{baseline:.6f}" textLength="365" '
                      f'lengthAdjust="spacingAndGlyphs">{"".join(spans)}</text>')
    return "\n".join(output + ["</g>"])


def field(key, value, y, x=390, end=970, value_markup=None):
    value = str(value)
    key_x = x + 19.2
    dots_x = key_x + (len(key) + 2) * 9.6
    value_x = end - len(value) * 9.6
    if value_x < dots_x:
        raise ValueError(f"Field does not fit in the profile card: {key}")
    dots = "." * max(0, int((value_x - dots_x) / 9.6) - 1)
    return (f'<text class="dots" x="{x}" y="{y}">.</text>'
            f'<text class="key" x="{key_x}" y="{y}">{escape(key)}'
            '<tspan class="ink">:</tspan></text>'
            f'<text class="dots" x="{dots_x}" y="{y}">{dots}</text>'
            f'<text class="value" x="{end}" y="{y}" text-anchor="end">'
            f'{value_markup if value_markup is not None else escape(value)}</text>')


def section(title, y, x=390, end=970):
    start = x + (len(title) + 1) * 9.6
    return (f'<text x="{x}" y="{y}">{escape(title)}</text>'
            f'<path d="M{start} {y - 5}H{end}" fill="none" stroke="currentColor" stroke-width="1"/>')


def desktop_fields(profile, stats, uptime, snapshot):
    output = [section(profile["header"], 30)]
    for index, item in enumerate(profile["fields"]):
        y = 50 + index * 20
        if item is None:
            output.append(f'<text class="dots" x="390" y="{y}">.</text>')
        else:
            key, value = item
            output.append(field(key, value.replace("{uptime}", uptime), y))
    contact_y = 70 + len(profile["fields"]) * 20
    if contact_y + len(profile["contact"]) * 20 >= 460:
        raise ValueError("Profile content overlaps the statistics section")
    output.append(section("- Contact", contact_y))
    for index, (key, value) in enumerate(profile["contact"], 1):
        output.append(field(key, value, contact_y + index * 20))
    output.append(section("- GitHub Stats", 480))
    repos, forks = f'{stats["repos"]:,}', f'{stats["forks"]:,}'
    fork_markup = (f'{repos}<tspan class="ink"> {{</tspan><tspan class="key">Forks</tspan>'
                   f'<tspan class="ink">: </tspan>{forks}<tspan class="ink">}}</tspan>')
    output.extend([
        field("Repos", f"{repos} {{Forks: {forks}}}", 500, end=710, value_markup=fork_markup),
        field("Stars", f'{stats["stars"]:,}', 500, x=745),
        field("Contributions.1y", f'{stats["contributions"]:,}', 520, end=710),
        field("Followers", f'{stats["followers"]:,}', 520, x=745),
        '<text x="724" y="500">|</text><text x="724" y="520">|</text>',
        field("Snapshot", snapshot.strftime("%Y-%m-%d %H:%M UTC+8"), 540),
    ])
    return "\n".join(output)


def mobile_fields(profile, stats, uptime, snapshot):
    output = [section(profile["header"], 580, x=18, end=402)]
    y = 600

    def add_field(key, value):
        nonlocal y
        value = str(value)
        if (len(key) + len(value) + 4) * 9.6 <= 384:
            output.append(field(key, value, y, x=18, end=402))
        else:
            if len(value) * 9.6 > 364:
                raise ValueError(f"Field does not fit in the mobile card: {key}")
            output.append(field(key, "", y, x=18, end=402))
            y += 20
            output.append(f'<text class="value" x="402" y="{y}" text-anchor="end">{escape(value)}</text>')
        y += 20

    for item in profile["fields"]:
        if item is None:
            y += 20
        else:
            key, value = item
            add_field(key, value.replace("{uptime}", uptime))
    y += 20
    output.append(section("- Contact", y, x=18, end=402))
    y += 20
    for key, value in profile["contact"]:
        add_field(key, value)
    y += 20
    output.append(section("- GitHub Stats", y, x=18, end=402))
    y += 20
    for key, count in (("Repos", "repos"), ("Forks", "forks"), ("Stars", "stars"),
                       ("Contributions.1y", "contributions"), ("Followers", "followers")):
        add_field(key, f'{stats[count]:,}')
    add_field("Snapshot", snapshot.strftime("%Y-%m-%d %H:%M UTC+8"))
    return "\n".join(output), y


def render_card(profile: dict, avatar: dict, stats: dict, theme: str, mobile: bool = False) -> str:
    colors = PALETTES[theme]
    snapshot = datetime.fromisoformat(stats["as_of"].replace("Z", "+00:00")).astimezone(LOCAL_TIME)
    created = datetime.fromisoformat(stats["created_at"].replace("Z", "+00:00")).astimezone(LOCAL_TIME)
    uptime = account_age(created.date(), snapshot.date())
    width, height = 985, 560
    portrait = render_avatar(avatar, theme == "dark")
    if mobile:
        width = 420
        fields, height = mobile_fields(profile, stats, uptime, snapshot)
        portrait = f'<g transform="translate(12.5 0)">{portrait}</g>'
    else:
        fields = desktop_fields(profile, stats, uptime, snapshot)
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title description" xml:space="preserve">',
        f'<title id="title">{escape(profile.get("name", profile["username"]))} — GitHub profile</title>',
        '<desc id="description">ASCII portrait with personal information and a public GitHub snapshot. '
        'Uptime is the GitHub account age. Repos and Stars exclude forks; Forks is separate. '
        'Contributions.1y is the total displayed by the public GitHub calendar.</desc>',
        '<style>text{font-family:Consolas,"Liberation Mono",monospace;'
        f'white-space:pre}}.ink{{fill:{colors["ink"]}}}.key{{fill:{colors["key"]}}}'
        f'.value{{fill:{colors["value"]}}}.dots{{fill:{colors["dots"]}}}</style>',
        f'<rect width="{width}" height="{height}" rx="15" fill="{colors["background"]}"/>',
        portrait,
        f'<g font-size="16" fill="{colors["ink"]}" color="{colors["ink"]}">{fields}</g></svg>\n',
    ])


def update(root: Path, offline: bool = False) -> dict:
    config = json.loads((root / "profile.json").read_text(encoding="utf-8"))
    assets = root / "assets"
    snapshot_path = assets / "github-stats.json"
    if offline:
        stats = json.loads(snapshot_path.read_text(encoding="utf-8"))
    else:
        stats = collect_stats(config["username"], datetime.now(timezone.utc), os.getenv("GITHUB_TOKEN", ""))
    avatar = json.loads((assets / "avatar.json").read_text(encoding="utf-8"))
    # Fetch and render everything before touching any generated artifact. The workflow
    # publishes all generated files together only after this command has succeeded.
    cards = {f'profile-{theme}{"-mobile" if mobile else ""}.svg':
             render_card(config, avatar, stats, theme, mobile)
             for theme in PALETTES for mobile in (False, True)}
    for filename, svg in cards.items():
        (assets / filename).write_text(svg, encoding="utf-8")
    snapshot_path.write_text(json.dumps(stats, indent=2) + "\n", encoding="utf-8")
    return stats


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="Regenerate from the saved snapshot")
    args = parser.parse_args()
    try:
        stats = update(ROOT, args.offline)
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"Profile update failed: {error}\n")
    print(f'Updated profile: {stats["repos"]} non-Fork repos, {stats["forks"]} forks, '
          f'{stats["stars"]} stars; snapshot {stats["as_of"]}')


if __name__ == "__main__":
    main()
