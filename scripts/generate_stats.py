"""Regenerate assets/stats-card.svg and assets/langs-card.svg from public GitHub data.

Uses only the standard library. Set GITHUB_TOKEN (the Actions token is enough) to
raise rate limits and to fetch the contribution count, which needs the GraphQL API.
Without a token, the contributions value is shown as an en dash.
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from svgkit import CHIP, INK2, doc, header_bar, slab, text, total_height

USER = "keerthanakulal"
ASSETS = Path(__file__).resolve().parent.parent / "assets"
DOC_W, W, FH = 380, 368, 276  # W is the card itself; DOC_W leaves a 12px gutter on one side
TOP_LANGS = 6
TOKEN = os.environ.get("GITHUB_TOKEN", "")


def request(url, data=None):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "profile-stats"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def api(path):
    return request(f"https://api.github.com{path}")


def search_count(kind):
    q = urllib.parse.quote(f"author:{USER} type:{kind}")
    return api(f"/search/issues?q={q}&per_page=1")["total_count"]


def contributions():
    if not TOKEN:
        return None
    query = ('query($u:String!){user(login:$u){contributionsCollection'
             '{contributionCalendar{totalContributions}}}}')
    body = json.dumps({"query": query, "variables": {"u": USER}}).encode()
    try:
        res = request("https://api.github.com/graphql", body)
        return res["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]
    except (urllib.error.URLError, KeyError, TypeError):
        return None


def collect():
    user = api(f"/users/{USER}")
    repos = []
    page = 1
    while True:
        chunk = api(f"/users/{USER}/repos?per_page=100&type=owner&page={page}")
        repos += chunk
        if len(chunk) < 100:
            break
        page += 1
    own = [r for r in repos if not r["fork"]]
    langs = {}
    for r in own:
        for lang, n in api(f"/repos/{USER}/{r['name']}/languages").items():
            langs[lang] = langs.get(lang, 0) + n
    return {
        "contributions": contributions(),
        "stars": sum(r["stargazers_count"] for r in own),
        "prs": search_count("pr"),
        "issues": search_count("issue"),
        "repos": user["public_repos"],
        "followers": user["followers"],
        "langs": sorted(langs.items(), key=lambda kv: -kv[1]),
    }


def stats_card(d):
    rows = [("Contributions (last year)", d["contributions"]), ("Stars earned", d["stars"]),
            ("Pull requests", d["prs"]), ("Issues", d["issues"]),
            ("Public repositories", d["repos"]), ("Followers", d["followers"])]
    body = header_bar("GitHub Stats")
    alt = []
    for i, (label, val) in enumerate(rows):
        y = 96 + i * 31
        v = "–" if val is None else f"{val:,}"
        body += (f'<circle cx="30" cy="{y - 5}" r="3.5" fill="url(#gAccent)"/>' + text(42, y, label, 15, 400, INK2) +
                 text(W - 24, y, v, 18, 700, anchor="end"))
        if i < len(rows) - 1:
            body += f'<rect x="24" y="{y + 11}" width="{W - 48}" height="1.5" rx=".75" fill="url(#gLine)"/>'
        alt.append(f"{label}: {'not available' if val is None else val}")
    return doc(DOC_W, total_height(FH), "GitHub stats for keerthanakulal. " + ". ".join(alt),
               slab(W, FH, body, delay=0, ox=0))


def langs_card(d):
    langs = d["langs"][:TOP_LANGS]
    total = sum(n for _, n in d["langs"]) or 1
    body = header_bar("Top Languages")
    alt = []
    bar_w = W - 48
    for i, (lang, n) in enumerate(langs):
        y = 94 + i * 29
        pct = n * 100 / total
        body += text(24, y, lang, 14.5) + text(W - 24, y, f"{pct:.1f}%", 14.5, 700, anchor="end")
        body += f'<rect x="24" y="{y + 7}" width="{bar_w}" height="9" rx="4.5" fill="{CHIP}"/>'
        body += (f'<rect class="gr" style="animation-delay:{i * .12:.2f}s" x="24" y="{y + 7}" '
                 f'width="{max(bar_w * pct / 100, 9):.1f}" height="9" rx="4.5" fill="url(#gAccent)"/>')
        alt.append(f"{lang} {pct:.1f}%")
    return doc(DOC_W, total_height(FH), "Top languages by code size across public repositories: " + ", ".join(alt),
               slab(W, FH, body, delay=0, ox=DOC_W - W))


def main():
    try:
        d = collect()
    except (urllib.error.URLError, KeyError) as e:
        print(f"GitHub API unavailable: {e}", file=sys.stderr)
        return 1
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "stats-card.svg").write_text(stats_card(d), encoding="utf-8", newline="\n")
    (ASSETS / "langs-card.svg").write_text(langs_card(d), encoding="utf-8", newline="\n")
    print("Updated stats-card.svg and langs-card.svg")
    return 0


if __name__ == "__main__":
    sys.exit(main())
