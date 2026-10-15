#!/usr/bin/env python3
"""Render the static, no-JavaScript-required Work index from site/data/work.json.

Run from the repository root:
  python tools/render_work.py
  python tools/render_work.py --check
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
DATA = SITE / "data" / "work.json"
TEMPLATE = ROOT / "tools" / "templates" / "work-index.html"
OUTPUT = SITE / "work" / "index.html"
EXPECTED_CATEGORIES = [
    ("decks", "Decks & Pitches"),
    ("interactive", "Interactive & 3D"),
    ("films", "Films"),
    ("brand-web", "Brand & Web"),
]
REQUIRED_PROJECT_FIELDS = {
    "id", "category", "title", "summary", "href", "linkLabel",
    "image", "width", "height", "alt", "disclosure",
}


def die(message: str) -> None:
    print(f"render_work.py: {message}", file=sys.stderr)
    raise SystemExit(1)


def esc(value: object, *, quote: bool = True) -> str:
    return html.escape(str(value), quote=quote)


def relative_url(url: str) -> str:
    """Make same-site root URLs work from /work/ and from a local HTTP preview."""
    if url.startswith("/"):
        return ".." + url
    return url


def local_path(url: str) -> Path | None:
    if not url.startswith("/") or url.startswith("//"):
        return None
    bare = url.split("#", 1)[0].split("?", 1)[0]
    if not bare or bare == "/":
        return SITE / "index.html"
    candidate = SITE / bare.lstrip("/")
    if bare.endswith("/"):
        candidate = candidate / "index.html"
    return candidate


def image_variant(image: str, width: int) -> str:
    path = PurePosixPath(image)
    return str(path.with_name(f"{path.stem}-{width}{path.suffix}"))


def render_links(project: dict[str, object]) -> str:
    main = (
        f'<a href="{esc(relative_url(str(project["href"])))}">'
        f'{esc(project["linkLabel"])}</a>'
    )
    links = [main]
    for link in project.get("secondaryLinks", []):
        if not isinstance(link, dict) or not {"label", "href"} <= set(link):
            die(f'{project["id"]}: malformed secondary link')
        attrs = ""
        if link.get("external"):
            attrs = ' target="_blank" rel="noopener"'
        links.append(
            f'<a href="{esc(relative_url(str(link["href"])))}"{attrs}>'
            f'{esc(link["label"])}</a>'
        )
    return "\n            ".join(links)


def render_card(project: dict[str, object], labels: dict[str, str]) -> str:
    missing = REQUIRED_PROJECT_FIELDS - set(project)
    if missing:
        die(f'{project.get("id", "project")}: missing {sorted(missing)}')
    category = str(project["category"])
    if category not in labels:
        die(f'{project["id"]}: unknown category {category!r}')
    image = str(project["image"])
    image_720 = image_variant(image, 720)
    image_1080 = image_variant(image, 1080)
    title_id = f'project-{project["id"]}'
    href = relative_url(str(project["href"]))
    return f'''<article class="work-card" data-category="{esc(category)}">
          <a class="work-card__media" href="{esc(href)}" aria-labelledby="{esc(title_id)}">
            <img class="shot" loading="lazy" decoding="async"
                 src="{esc(relative_url(image))}"
                 srcset="{esc(relative_url(image_720))} 720w, {esc(relative_url(image_1080))} 1080w, {esc(relative_url(image))} {esc(project["width"])}w"
                 sizes="(min-width: 68rem) 22rem, (min-width: 44rem) 46vw, 92vw"
                 width="{esc(project["width"])}" height="{esc(project["height"])}"
                 alt="{esc(project["alt"])}">
          </a>
          <div class="work-card__body">
            <span class="work-card__category">{esc(labels[category])}</span>
            <h2 id="{esc(title_id)}"><a href="{esc(href)}">{esc(project["title"])}</a></h2>
            <p class="work-card__summary">{esc(project["summary"])}</p>
            <p class="work-card__links">
            {render_links(project)}
            </p>
            <p class="label">{esc(project["disclosure"])}</p>
          </div>
        </article>'''


def validate_local_reference(project_id: str, url: str, role: str) -> None:
    path = local_path(url)
    if path is not None and not path.is_file():
        die(f"{project_id}: {role} does not exist: {url} -> {path.relative_to(ROOT)}")


def render() -> str:
    try:
        data = json.loads(DATA.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        die(f"cannot read {DATA.relative_to(ROOT)}: {exc}")

    categories = [(item.get("id"), item.get("label")) for item in data.get("categories", [])]
    if categories != EXPECTED_CATEGORIES:
        die(f"categories must be exactly {EXPECTED_CATEGORIES}; got {categories}")
    labels = dict(EXPECTED_CATEGORIES)
    projects = data.get("projects")
    if not isinstance(projects, list) or not projects:
        die("projects must be a non-empty list")

    seen_ids: set[str] = set()
    for project in projects:
        if not isinstance(project, dict):
            die("every project must be an object")
        project_id = str(project.get("id", ""))
        if not project_id or project_id in seen_ids:
            die(f"project id is missing or duplicated: {project_id!r}")
        seen_ids.add(project_id)
        if set(project) - (REQUIRED_PROJECT_FIELDS | {"secondaryLinks"}):
            die(f"{project_id}: unexpected fields {sorted(set(project) - (REQUIRED_PROJECT_FIELDS | {'secondaryLinks'}))}")
        validate_local_reference(project_id, str(project.get("href", "")), "destination")
        image = str(project.get("image", ""))
        for label, url in (
            ("image", image),
            ("720px image", image_variant(image, 720)),
            ("1080px image", image_variant(image, 1080)),
        ):
            validate_local_reference(project_id, url, label)
        for link in project.get("secondaryLinks", []):
            if isinstance(link, dict) and not link.get("external"):
                validate_local_reference(project_id, str(link.get("href", "")), "secondary destination")

    home = (SITE / "index.html").read_text(encoding="utf-8")
    brand = re.search(r"<!--BRAND:LOCKUP-->.*?<!--/BRAND:LOCKUP-->", home, re.S)
    if not brand:
        die("brand lockup markers are missing from site/index.html")

    filters = "\n        ".join(
        f'<button class="work-filter" type="button" data-filter="{esc(category_id)}" '
        f'aria-pressed="false" aria-controls="work-grid">{esc(label)}</button>'
        for category_id, label in EXPECTED_CATEGORIES
    )
    cards = "\n        ".join(render_card(project, labels) for project in projects)
    template = TEMPLATE.read_text(encoding="utf-8")
    output = (
        template
        .replace("{{BRAND_LOCKUP}}", brand.group(0))
        .replace("{{WORK_FILTERS}}", filters)
        .replace("{{WORK_CARDS}}", cards)
        .replace("{{WORK_COUNT}}", str(len(projects)))
    )
    leftovers = re.findall(r"{{[A-Z_]+}}", output)
    if leftovers:
        die(f"unresolved template placeholders: {leftovers}")
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if the generated page is stale")
    args = parser.parse_args()
    output = render()
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != output:
            die(f"{OUTPUT.relative_to(ROOT)} is stale; run python tools/render_work.py")
        print(f"render_work.py: {OUTPUT.relative_to(ROOT)} is current ({output.count('class=\"work-card\"')} projects)")
        return
    OUTPUT.write_text(output, encoding="utf-8", newline="\n")
    print(f"render_work.py: wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
