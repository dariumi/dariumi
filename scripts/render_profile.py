#!/usr/bin/env python3
import html
import json
import os
import urllib.request
from pathlib import Path

OWNER = "dariumi"

PROJECTS = [
    {
        "repo": "Daria",
        "file": "daria.svg",
        "index": "01",
        "title": "DARIA",
        "subtitle": "local AI companion",
        "icon": """<g transform="translate(448 90)" fill="none" stroke-width="1.5">
<circle class="line" r="44"/><circle class="accentLine" r="22"/><circle class="accent" r="5" stroke="none"/>
<path class="line" d="M0-44V-64M44 0h34M0 44v28M-44 0h-28"/>
</g>""",
    },
    {
        "repo": "veil",
        "file": "veil.svg",
        "index": "02",
        "title": "veil",
        "subtitle": "private network layer",
        "icon": """<g transform="translate(446 90)" fill="none" stroke-width="1.5">
<path class="line" d="M-54-34C-10-54 12-6 54-28M-54 2C-8-18 12 30 54 8M-54 38C-10 18 12 66 54 44"/>
<path class="accentLine" d="M-60-50L60 58M60-50L-60 58"/>
<circle class="accent" cx="0" cy="4" r="5" stroke="none"/>
</g>""",
    },
    {
        "repo": "Daphne",
        "file": "daphne.svg",
        "index": "03",
        "title": "Daphne",
        "subtitle": "data tooling",
        "icon": """<g transform="translate(446 90)" fill="none" stroke-width="1.5">
<rect class="line" x="-48" y="-46" width="96" height="24" rx="6"/>
<rect class="line" x="-38" y="-10" width="76" height="24" rx="6"/>
<rect class="line" x="-28" y="26" width="56" height="24" rx="6"/>
<path class="accentLine" d="M-56 0H56"/>
</g>""",
    },
    {
        "repo": "Arkonova-Network",
        "file": "arkonova.svg",
        "index": "04",
        "title": "Arkonova",
        "subtitle": "experiments / infrastructure",
        "icon": """<g transform="translate(446 90)" fill="none" stroke-width="1.5">
<path class="line" d="M-52-30L0-58L48-22L38 38L-16 56L-54 18Z"/>
<path class="line" d="M-52-30L38 38M0-58L-16 56M48-22L-54 18"/>
<circle class="accent" cx="0" cy="-58" r="5" stroke="none"/>
<circle class="accent" cx="38" cy="38" r="5" stroke="none"/>
<circle class="accent" cx="-54" cy="18" r="5" stroke="none"/>
</g>""",
    },
]

STYLE = """.bg{fill:#f7f8fa}.fg{fill:#111318}.muted{fill:#727987}.line{stroke:#cfd4dc}.accent{fill:#7c6cf2}.accentLine{stroke:#7c6cf2}.chip{fill:#eceafd}
@media(prefers-color-scheme:dark){.bg{fill:#0b0d10}.fg{fill:#f3f5f7}.muted{fill:#8d95a3}.line{stroke:#2a3039}.accent{fill:#9b8cff}.accentLine{stroke:#9b8cff}.chip{fill:#171525}}
text{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono",monospace}"""

def fetch_repo(name):
    url = f"https://api.github.com/repos/{OWNER}/{name}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "dariumi-profile-renderer",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.load(response)

def render(project, meta):
    stars = meta.get("stargazers_count", 0)
    language = meta.get("language") or "mixed"
    title = html.escape(project["title"])
    subtitle = html.escape(project["subtitle"])
    language = html.escape(str(language))
    return f"""<svg width="560" height="180" viewBox="0 0 560 180" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{title}">
<defs><style>{STYLE}</style></defs>
<rect class="bg" width="560" height="180" rx="20"/>
<text class="muted" x="26" y="34" font-size="12" letter-spacing="3">{project["index"]}</text>
<rect class="chip" x="26" y="49" width="94" height="24" rx="12"/>
<text class="fg" x="73" y="65" text-anchor="middle" font-size="11">★ {stars}</text>
<text class="muted" x="132" y="65" font-size="11">{language}</text>
<text class="fg" x="26" y="112" font-size="30" font-weight="700">{title}</text>
<text class="muted" x="26" y="142" font-size="13">{subtitle}</text>
{project["icon"]}
</svg>"""

def main():
    assets = Path("assets")
    assets.mkdir(exist_ok=True)
    for project in PROJECTS:
        try:
            meta = fetch_repo(project["repo"])
        except Exception as exc:
            print(f"warning: {project['repo']}: {exc}")
            meta = {"stargazers_count": "?", "language": "unknown"}
        out = assets / project["file"]
        content = render(project, meta)
        if not out.exists() or out.read_text(encoding="utf-8") != content:
            out.write_text(content, encoding="utf-8")
            print(f"updated {out}")
        else:
            print(f"unchanged {out}")

if __name__ == "__main__":
    main()
