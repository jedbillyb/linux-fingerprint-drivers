#!/usr/bin/env python3
"""Render the repo's markdown into a static site for GitHub Pages.

    pip install markdown
    python3 tools/build-site.py [--out site] [--base-url ''] [--cname host]

Why this exists: essentially everyone who reaches this repo arrives from a
search engine having typed a laptop model or a USB ID, and GitHub's own blob
pages index poorly. One real HTML page per sensor, with a title and description
naming the ID, the chip and the machines it ships in, is the difference between
being findable and not.

The site is generated, never committed. Every page is built from the same
markdown that GitHub renders, so there is only one copy of the content.
"""

from __future__ import annotations

import argparse
import html
import re
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import quote, urlparse

REPO = Path(__file__).resolve().parent.parent
GITHUB = "https://github.com/jedbillyb/linux-fingerprint-drivers"
GITHUB_BLOB = GITHUB + "/blob/master/"
GITHUB_TREE = GITHUB + "/tree/master/"

USB_ID = re.compile(r"^[0-9a-f]{4}:[0-9a-f]{4}$")
TITLE = re.compile(r"^#\s+(.+?)\s*$", re.M)
STATUS = re.compile(r"^\*\*Status:\s*(.+?)\*\*\s*$", re.M | re.I)
MD_LINK = re.compile(r"(?<!\!)\[([^\]]*)\]\(([^)\s]+)(\s+\"[^\"]*\")?\)")
FIRST_PROSE = re.compile(r"^(?![#>|\-*`])\S.*$", re.M)


@dataclass
class Page:
    """One rendered HTML page and everything the templates need about it."""
    source: Path                  # repo-relative markdown path
    url_path: str                 # site path, no leading or trailing slash
    title: str                    # <title>
    heading: str                  # visible h1 (comes from the markdown itself)
    description: str
    markdown: str
    models: list[str] = field(default_factory=list)
    usb_ids: list[str] = field(default_factory=list)
    priority: str = "0.5"


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def squash(text: str) -> str:
    """Markdown prose to a single clean line for a meta description."""
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = MD_LINK.sub(r"\1", text)
    text = re.sub(r"\*\*([^*]*)\*\*", r"\1", text)
    text = re.sub(r"[*_>]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def clip(text: str, limit: int = 158) -> str:
    text = squash(text)
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0]
    return cut.rstrip(" .,;:") + "..."


def sensor_name(title: str) -> str:
    return re.sub(r"\s*\((?:USB|PID)[^)]*\)\s*$", "", title).strip()


def read_models(entry: Path) -> list[str]:
    f = entry / "MODELS"
    if not f.is_file():
        return []
    return [ln.strip() for ln in f.read_text(encoding="utf-8").splitlines()
            if ln.strip() and not ln.startswith("#")]


def collect_pages() -> list[Page]:
    pages: list[Page] = []

    readme = (REPO / "README.md").read_text(encoding="utf-8")
    pages.append(Page(
        source=Path("README.md"),
        url_path="",
        title="Linux fingerprint reader drivers: sensors libfprint does not support",
        heading="linux-fingerprint-drivers",
        description=(
            "Community catalogue of drivers, patches and setup notes for fingerprint "
            "readers that upstream libfprint does not support. Find your sensor by "
            "USB ID or laptop model."
        ),
        markdown=readme,
        priority="1.0",
    ))

    contributing = REPO / "CONTRIBUTING.md"
    if contributing.is_file():
        text = contributing.read_text(encoding="utf-8")
        pages.append(Page(
            source=Path("CONTRIBUTING.md"),
            url_path="contributing",
            title="Contributing a fingerprint sensor entry or report",
            heading=heading_of(text, "Contributing"),
            description=clip(first_prose(text)),
            markdown=text,
            priority="0.3",
        ))

    for doc in sorted((REPO / "docs").glob("*.md")):
        text = doc.read_text(encoding="utf-8")
        name = doc.stem
        head = heading_of(text, name)
        if name == "laptops":
            title = "Fingerprint reader support on Linux by laptop model"
            desc = ("Which laptops have fingerprint readers that work on Linux, indexed "
                    "by model: ThinkPad, XPS, EliteBook, ProBook, Latitude, MagicBook "
                    "and more, with the USB ID and driver route for each.")
            priority = "0.9"
        elif name == "unsupported-devices":
            title = "Fingerprint sensors with no Linux driver (contributor gap-map)"
            desc = clip(first_prose(text))
            priority = "0.6"
        elif name == "BUILD":
            title = "Building libfprint from source for an unsupported fingerprint reader"
            desc = ("Build, install, PAM setup, package pinning, troubleshooting and "
                    "revert steps for running a patched libfprint on Arch, Fedora, "
                    "Debian and Ubuntu.")
            priority = "0.7"
        else:
            title = head
            desc = clip(first_prose(text))
            priority = "0.5"
        pages.append(Page(
            source=Path("docs") / doc.name,
            url_path=f"docs/{slug(name)}",
            title=title,
            heading=head,
            description=desc,
            markdown=text,
            priority=priority,
        ))

    for entry in sorted(p for p in (REPO / "devices").iterdir() if p.is_dir()):
        md = entry / "README.md"
        if not md.is_file():
            continue
        text = md.read_text(encoding="utf-8")
        head = heading_of(text, entry.name)
        chip = sensor_name(head)
        models = read_models(entry)
        ids = sorted(set(re.findall(r"\b[0-9a-f]{4}:[0-9a-f]{4}\b", head)))
        if USB_ID.match(entry.name) and entry.name not in ids:
            ids.insert(0, entry.name)

        if USB_ID.match(entry.name):
            title = f"{entry.name} fingerprint reader on Linux: {chip}"
        else:
            title = f"{chip}: fingerprint reader support on Linux"
        if models:
            title += " (" + ", ".join(models[:2]) + ")"

        status = STATUS.search(text)
        bits = []
        if status:
            bits.append(squash(status.group(1)).rstrip("."))
        if models:
            bits.append("Seen on " + ", ".join(models[:4]))
        bits.append(clip(first_prose(text), 90))
        pages.append(Page(
            source=Path("devices") / entry.name / "README.md",
            url_path=f"devices/{slug(entry.name)}",
            title=title,
            heading=head,
            description=clip(". ".join(b for b in bits if b)),
            markdown=text,
            models=models,
            usb_ids=ids,
            priority="0.8",
        ))

    return pages


def heading_of(text: str, fallback: str) -> str:
    m = TITLE.search(text)
    return m.group(1).strip() if m else fallback


def first_prose(text: str) -> str:
    body = TITLE.sub("", text, count=1)
    for line in FIRST_PROSE.finditer(body):
        candidate = line.group(0).strip()
        if len(candidate) > 40:
            # Grab the rest of that paragraph so the description is a sentence.
            rest = body[line.start():].split("\n\n", 1)[0]
            return rest
    return squash(body)[:200]


def build_link_map(pages: list[Page]) -> dict[str, str]:
    """Repo-relative source path -> site path, plus the directory forms of it."""
    out: dict[str, str] = {}
    for page in pages:
        src = page.source.as_posix()
        out[src] = page.url_path
        if src.endswith("/README.md"):
            out[src[: -len("README.md")]] = page.url_path       # 'devices/x/'
            out[src[: -len("/README.md")]] = page.url_path      # 'devices/x'
        elif src == "README.md":
            out["."] = page.url_path
    return out


def rewrite_links(page: Page, link_map: dict[str, str], base: str) -> str:
    """Point internal markdown links at the built site, everything else at GitHub."""
    src_dir = page.source.parent

    def resolve(target: str) -> str:
        if not target or target.startswith("#"):
            return target
        parsed = urlparse(target)
        if parsed.scheme or target.startswith("//") or target.startswith("mailto:"):
            return target

        path, _, anchor = target.partition("#")
        anchor = f"#{anchor}" if anchor else ""
        if not path:
            return target

        try:
            resolved = (src_dir / path).resolve().relative_to(REPO).as_posix()
        except (ValueError, OSError):
            return target
        trailing = "/" if path.endswith("/") else ""

        for key in (resolved + trailing, resolved, resolved + "/"):
            if key in link_map:
                dest = link_map[key]
                return f"{base}/{dest}/{anchor}" if dest else f"{base}/{anchor}"

        # Not a rendered page: a patch, a CREDITS file, a directory of them.
        abs_path = REPO / resolved
        prefix = GITHUB_TREE if abs_path.is_dir() else GITHUB_BLOB
        return prefix + quote(resolved) + anchor

    def sub(m: re.Match[str]) -> str:
        return f"[{m.group(1)}]({resolve(m.group(2))}{m.group(3) or ''})"

    return MD_LINK.sub(sub, page.markdown)


STYLE = """
:root{--bg:#fff;--fg:#1c1e21;--muted:#5b616b;--line:#d8dce1;--accent:#0b5fd0;
--code-bg:#f4f6f8;--card:#f8f9fb;--ok:#1a7f4b;--warn:#8a5a00;--bad:#a32020}
@media (prefers-color-scheme:dark){:root{--bg:#0f1115;--fg:#e6e8ec;--muted:#9aa3ad;
--line:#2a2f37;--accent:#6aa8ff;--code-bg:#161a20;--card:#141821;--ok:#4cc38a;
--warn:#d9a441;--bad:#f2777a}}
*{box-sizing:border-box}
/* No rubber-band overscroll past the header or footer. The background is set
   on html as well so the browser has nothing of its own to paint if a platform
   bounces anyway. */
html{overscroll-behavior-y:none;background:var(--bg)}
body{margin:0;background:var(--bg);color:var(--fg);overscroll-behavior-y:none;
font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.wrap{max-width:52rem;margin:0 auto;padding:1.25rem 1.15rem 4rem}
header.site{border-bottom:1px solid var(--line);margin-bottom:1.75rem}
header.site .wrap{padding-bottom:.85rem;padding-top:.85rem}
nav a{margin-right:1rem;white-space:nowrap}
nav{display:flex;flex-wrap:wrap;gap:.15rem .25rem;font-size:.94rem}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
h1{font-size:1.75rem;line-height:1.25;margin:0 0 .6rem}
h2{font-size:1.3rem;margin:2.2rem 0 .7rem;padding-top:.3rem;border-top:1px solid var(--line)}
h3{font-size:1.08rem;margin:1.6rem 0 .5rem}
code{background:var(--code-bg);padding:.12em .34em;border-radius:4px;
font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.9em}
pre{background:var(--code-bg);padding:.85rem 1rem;border-radius:8px;overflow-x:auto;
border:1px solid var(--line)}
pre code{background:none;padding:0;font-size:.86rem}
.table-wrap{overflow-x:auto;margin:1rem 0}
table{border-collapse:collapse;width:100%;font-size:.92rem}
th,td{border:1px solid var(--line);padding:.45rem .6rem;text-align:left;vertical-align:top}
th{background:var(--card);font-weight:600}
blockquote{margin:1rem 0;padding:.1rem 1rem;border-left:3px solid var(--line);color:var(--muted)}
.meta{background:var(--card);border:1px solid var(--line);border-radius:8px;
padding:.85rem 1rem;margin:0 0 1.5rem;font-size:.94rem}
.meta dl{display:grid;grid-template-columns:auto 1fr;gap:.35rem .9rem;margin:0}
.meta dt{color:var(--muted);font-weight:600}
.meta dd{margin:0}
footer.site{border-top:1px solid var(--line);margin-top:3rem;padding-top:1rem;
color:var(--muted);font-size:.88rem}
footer.site p{margin:0 0 .6rem}
footer.site p:last-child{margin-bottom:0}
footer.site .credit{padding-top:.6rem;border-top:1px solid var(--line)}
.breadcrumb{color:var(--muted);font-size:.88rem;margin-bottom:.5rem}
img{max-width:100%}
"""


def nav_html(base: str) -> str:
    items = [
        ("Home", f"{base}/"),
        ("Find your laptop", f"{base}/docs/laptops/"),
        ("Build guide", f"{base}/docs/build/"),
        ("Gap-map", f"{base}/docs/unsupported-devices/"),
        ("Contributing", f"{base}/contributing/"),
        ("GitHub", GITHUB),
    ]
    return "".join(f'<a href="{html.escape(u)}">{html.escape(t)}</a>' for t, u in items)


def meta_block(page: Page, base: str) -> str:
    """The at-a-glance box on a device page: IDs, machines, source file."""
    if not page.source.parts[:1] == ("devices",):
        return ""
    rows = []
    if page.usb_ids:
        rows.append(("USB ID", ", ".join(f"<code>{html.escape(i)}</code>"
                                         for i in page.usb_ids)))
    if page.models:
        rows.append(("Reported in", html.escape(", ".join(page.models))))
    rows.append((
        "Source",
        f'<a href="{GITHUB_BLOB}{quote(page.source.as_posix())}">'
        f'{html.escape(page.source.as_posix())}</a>',
    ))
    body = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows)
    return f'<div class="meta"><dl>{body}</dl></div>'


def render_page(page: Page, body_html: str, base: str, site_url: str) -> str:
    canonical = f"{site_url}/{page.url_path}/" if page.url_path else f"{site_url}/"
    crumb = ""
    if page.url_path:
        crumb = (f'<div class="breadcrumb"><a href="{base}/">'
                 f"linux-fingerprint-drivers</a> / {html.escape(page.heading)}</div>")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(page.title)}</title>
<meta name="description" content="{html.escape(page.description)}">
<link rel="canonical" href="{html.escape(canonical)}">
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(page.title)}">
<meta property="og:description" content="{html.escape(page.description)}">
<meta property="og:url" content="{html.escape(canonical)}">
<meta name="twitter:card" content="summary">
<style>{STYLE}</style>
</head>
<body>
<header class="site"><div class="wrap"><nav>{nav_html(base)}</nav></div></header>
<main class="wrap">
{crumb}
{meta_block(page, base)}
{body_html}
</main>
<footer class="site"><div class="wrap">
<p>Community catalogue of Linux fingerprint reader drivers.
Content mirrors <a href="{GITHUB}">the repository</a>; hosted code is LGPL-2.1.
Always check <a href="https://fprint.freedesktop.org/supported-devices.html">upstream
libfprint</a> first.</p>
<p><strong>The drivers and patches catalogued here are the work of their
individual authors</strong>, credited in each entry and in the upstream merge
requests. If an entry helped you, thank them: report back on the
<a href="{GITHUB}/issues">issue tracker</a> so the status stays honest, or send a
fix upstream to
<a href="https://gitlab.freedesktop.org/libfprint/libfprint">libfprint</a>.</p>
<p class="credit">This catalogue is maintained by
<a href="https://jedbillyb.com">Jed Blenkhorn</a>
&middot; <a href="https://github.com/jedbillyb">GitHub</a>
&middot; <a href="https://buymeacoffee.com/jedbillyb">buy me a coffee</a>
if it saved you an evening.</p>
</div></footer>
</body>
</html>
"""


def wrap_tables(body: str) -> str:
    """Tables must scroll inside themselves, not push the page sideways."""
    return body.replace("<table>", '<div class="table-wrap"><table>') \
               .replace("</table>", "</table></div>")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="site")
    # Served from its own hostname, so pages sit at the root rather than under
    # a /linux-fingerprint-drivers/ path prefix.
    ap.add_argument("--base-url", default="")
    ap.add_argument("--site-url", default="https://fprint.jedbillyb.com")
    ap.add_argument("--cname", default="fprint.jedbillyb.com",
                    help="custom domain written to site/CNAME; empty to omit")
    args = ap.parse_args()

    try:
        import markdown
    except ImportError:
        print("this needs the 'markdown' package: pip install markdown", file=sys.stderr)
        return 1

    base = args.base_url.rstrip("/")
    site_url = args.site_url.rstrip("/")
    out = (REPO / args.out) if not Path(args.out).is_absolute() else Path(args.out)
    if out.exists():
        shutil.rmtree(out)

    pages = collect_pages()
    link_map = build_link_map(pages)
    md = markdown.Markdown(extensions=["tables", "fenced_code", "toc", "sane_lists"])

    for page in pages:
        md.reset()
        body = wrap_tables(md.convert(rewrite_links(page, link_map, base)))
        target = out / page.url_path / "index.html" if page.url_path else out / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_page(page, body, base, site_url), encoding="utf-8")

    urls = "".join(
        "<url><loc>{}</loc><priority>{}</priority></url>".format(
            f"{site_url}/{p.url_path}/" if p.url_path else f"{site_url}/", p.priority)
        for p in pages
    )
    (out / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"{urls}</urlset>\n",
        encoding="utf-8",
    )
    (out / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {site_url}/sitemap.xml\n", encoding="utf-8")
    # Jekyll would otherwise eat directories it considers special.
    (out / ".nojekyll").write_text("", encoding="utf-8")
    # With Actions-based publishing the custom domain comes from the repository's
    # Pages settings, not from this file, so writing it does not configure
    # anything on its own. It is kept because it documents the intended hostname
    # next to the build, and because a branch-based deploy would need it.
    if args.cname:
        (out / "CNAME").write_text(args.cname + "\n", encoding="utf-8")

    print(f"built {len(pages)} pages into {out.relative_to(REPO) if out.is_relative_to(REPO) else out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
