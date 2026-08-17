#!/usr/bin/env python3
"""Generate docs/laptops.md, the by-laptop-model index.

    python3 tools/gen-laptop-index.py            # rewrite docs/laptops.md
    python3 tools/gen-laptop-index.py --check    # fail if it is out of date

Most people arrive knowing their laptop, not their USB ID. This builds a model
-> USB ID -> entry index from two sources that already exist in the repo, so it
cannot drift from them:

  * devices/<id>/MODELS  - one laptop model per line, for catalogued sensors
  * docs/unsupported-devices.md - the gap-map's Hardware column

Nothing here is hand-written, so a new MODELS line is all it takes to appear.
"""

from __future__ import annotations

import difflib
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEVICES = REPO / "devices"
GAP_MAP = REPO / "docs" / "unsupported-devices.md"
OUT = REPO / "docs" / "laptops.md"

# Row order within the page: the statuses people can act on come first.
STATUS_ORDER = {
    "Working": 0,
    "Working (vendor blob)": 1,
    "Partial": 2,
    "Merged upstream": 3,
    "WIP": 4,
    "Unreliable": 5,
    "Stale": 6,
    "No known fix": 7,
}

# Matched against the whole model string, first hit wins, so put the
# distinctive product lines before the bare vendor names.
VENDORS: list[tuple[str, tuple[str, ...]]] = [
    ("Lenovo", ("thinkpad", "thinkbook", "ideapad", "legion", "yoga", "lenovo")),
    ("Dell", ("xps", "latitude", "precision", "inspiron", "vostro", "alienware", "dell")),
    ("HP", ("elitebook", "probook", "zbook", "pavilion", "envy", "spectre", "omen",
            "victus", "hp ", "hp-")),
    ("Asus", ("zenbook", "vivobook", "expertbook", "rog ", "tuf ", "asus")),
    ("Acer", ("aspire", "swift", "nitro", "predator", "travelmate", "acer")),
    ("Samsung", ("galaxy book", "samsung")),
    ("Huawei", ("matebook", "huawei")),
    ("Honor", ("magicbook", "honor")),
    ("Xiaomi / Redmi", ("redmibook", "redmi", "xiaomi", "mi notebook", "mi ")),
    ("Framework", ("framework",)),
    ("Microsoft Surface", ("surface",)),
    ("MSI", ("katana", "modern", "prestige", "msi")),
    ("LG", ("lg gram", "gram ")),
    ("Handhelds and mini PCs", ("gpd win", "ayaneo", "gtr5", "steam deck", "onexplayer")),
    ("Chromebooks", ("chromebook",)),
    ("Other vendors", ("realme", "canvasbio", "tuxedo", "system76", "clevo", "medion",
                       "fujitsu", "toshiba", "panasonic", "gigabyte", "razer",
                       "teclast", "chuwi", "vaio", "dynabook")),
]

# Gap-map Hardware cells that name no machine, or name a peripheral rather
# than a laptop (the upstream wiki has a few of both).
PLACEHOLDER = re.compile(r"^(-|n/?a|external(\s*\(usb\))?|unknown|\?)$", re.I)
NOT_A_LAPTOP = re.compile(r"\b(mouse|keyboard|dongle|hub)\b", re.I)

# The gap-map writes an ID either as a wiki link or as bare code, depending on
# whether that device has a wiki page that actually exists, so accept both:
#   | [04f3:0c57](https://.../04f3:0c57) | Lenovo IdeaPad 3-15ARE05 |  |
#   | `04f3:0c5a`                        | Surface Laptop Go        |  |
GAP_ROW = re.compile(
    r"^\|\s*[`\[]?([0-9a-f]{4}:[0-9a-f]{4})[`\]]?[^|]*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*$"
)
TITLE = re.compile(r"^#\s+(.+?)\s*$", re.M)
STATUS = re.compile(r"^\*\*Status:\s*(.+?)\*\*\s*$", re.M | re.I)


def classify(status_text: str) -> str:
    """Collapse each entry's prose status line into one comparable word."""
    low = status_text.lower()
    if low.startswith("merged"):
        return "Merged upstream"
    if low.startswith("stale"):
        return "Stale"
    if low.startswith("partial"):
        return "Partial"
    if low.startswith("claimed"):
        return "Unreliable"
    if low.startswith("wip"):
        return "WIP"
    if low.startswith(("working", "works")):
        # A vendor blob route works, but it is not the same offer as open code.
        if "proprietary" in low or "vendor" in low or "agpl" in low:
            return "Working (vendor blob)"
        return "Working"
    return "WIP"


def vendor_of(model: str) -> str:
    low = model.lower()
    for name, keys in VENDORS:
        if any(k in low for k in keys):
            return name
    return "Other and unidentified"


def sensor_name(title: str) -> str:
    """Strip the '(USB ....)' tail from an entry title to get the chip name."""
    return re.sub(r"\s*\((?:USB|PID)[^)]*\)\s*$", "", title).strip()


def read_entries() -> list[dict]:
    rows: list[dict] = []
    for entry in sorted(p for p in DEVICES.iterdir() if p.is_dir()):
        models_file = entry / "MODELS"
        if not models_file.is_file():
            continue
        readme = (entry / "README.md").read_text(encoding="utf-8")
        title = TITLE.search(readme)
        status = STATUS.search(readme)
        if not title or not status:
            print(f"warning: {entry.name} has no title or status line", file=sys.stderr)
            continue
        sensor = sensor_name(title.group(1))
        state = classify(status.group(1))
        for line in models_file.read_text(encoding="utf-8").splitlines():
            model = line.strip()
            if not model or model.startswith("#"):
                continue
            rows.append({
                "model": model,
                "id": entry.name,
                "sensor": sensor,
                "status": state,
                "link": f"../devices/{entry.name}/",
            })
    return rows


def read_gap_map() -> list[dict]:
    rows: list[dict] = []
    for line in GAP_MAP.read_text(encoding="utf-8").splitlines():
        m = GAP_ROW.match(line)
        if not m:
            continue
        usb_id, hardware, lead = m.group(1), m.group(2).strip(), m.group(3).strip()
        if not hardware or PLACEHOLDER.match(hardware) or NOT_A_LAPTOP.search(hardware):
            continue
        rows.append({
            "model": hardware,
            "id": usb_id,
            "sensor": "lead: " + lead if lead else "",
            "status": "No known fix",
            "link": "unsupported-devices.md",
        })
    return rows


def render(rows: list[dict]) -> str:
    covered = sum(1 for r in rows if r["status"] != "No known fix")
    out: list[str] = []
    add = out.append

    add("# Find your laptop")
    add("")
    add("Fingerprint reader support on Linux, indexed by **laptop model** rather")
    add("than by USB ID. If `fprintd-enroll` fails on your machine, find it below.")
    add("")
    add("This page is generated from the device entries and the")
    add("[gap-map](unsupported-devices.md); it lists every model those name, and")
    add("nothing else. Absence from this page is not evidence that a reader works")
    add("or does not: it usually just means nobody has reported that model yet.")
    add("Many sensors also ship in machines nobody has written down here, so if")
    add("your exact model is missing, **match on the USB ID instead**:")
    add("")
    add("```sh")
    add("lsusb        # find the reader, e.g. 27c6:55b4")
    add("```")
    add("")
    add("then look it up in the [main README](../README.md), or run")
    add("`./tools/detect.sh` to have it matched for you.")
    add("")
    add(f"{covered} model listings map to a catalogued sensor; the rest are on the")
    add("gap-map with no known fix, and a protocol dump for any of them is welcome.")
    add("")
    add("**Adding your machine** is the single most useful small contribution here.")
    add("Open a [device report](https://github.com/jedbillyb/linux-fingerprint-drivers/issues/new?template=device-report.yml)")
    add("with your model and `lsusb` line, or add a line to the sensor's")
    add("`devices/<id>/MODELS` file and open a PR.")
    add("")
    add("Status legend: **Working** (enroll and verify reliable), **Working (vendor")
    add("blob)** (only via a proprietary driver, see the entry's caveats),")
    add("**Partial**, **Merged upstream** (in libfprint git, build from source),")
    add("**WIP** (unmerged work exists), **Unreliable** (claimed upstream but fails")
    add("in practice), **Stale** (abandoned lead), **No known fix**.")
    add("")

    groups: dict[str, list[dict]] = {}
    for row in rows:
        groups.setdefault(vendor_of(row["model"]), []).append(row)

    order = [name for name, _ in VENDORS] + ["Other and unidentified"]
    for vendor in order:
        items = groups.get(vendor)
        if not items:
            continue
        items.sort(key=lambda r: (STATUS_ORDER[r["status"]], r["model"].lower()))
        add(f"## {vendor}")
        add("")
        if vendor == "Other and unidentified":
            add("Rows the upstream wiki records against a chip or module name")
            add("rather than a machine. Match these on the USB ID.")
            add("")
        add("| Laptop model | USB ID | Sensor | Status | Where to go |")
        add("|--------------|--------|--------|--------|-------------|")
        for r in items:
            sensor = r["sensor"] or "-"
            where = "[entry](%s)" % r["link"] if r["status"] != "No known fix" \
                else "[gap-map](unsupported-devices.md)"
            add(f"| {r['model']} | `{r['id']}` | {sensor} | {r['status']} | {where} |")
        add("")

    add("---")
    add("")
    add("_Generated by `tools/gen-laptop-index.py`. Do not edit by hand: edit a")
    add("`devices/<id>/MODELS` file or the gap-map and regenerate._")
    add("")
    return "\n".join(out)


def main() -> int:
    rows = read_entries() + read_gap_map()
    if not rows:
        print("no models found; is devices/*/MODELS missing?", file=sys.stderr)
        return 1
    text = render(rows)

    if "--check" in sys.argv:
        current = OUT.read_text(encoding="utf-8") if OUT.is_file() else ""
        if current != text:
            print(
                "docs/laptops.md is out of date; run: python3 tools/gen-laptop-index.py",
                file=sys.stderr,
            )
            # Show what differs, so a CI failure is diagnosable from the log
            # rather than only reproducible by rerunning the generator.
            diff = difflib.unified_diff(
                current.splitlines(keepends=True),
                text.splitlines(keepends=True),
                fromfile="docs/laptops.md (committed)",
                tofile="docs/laptops.md (regenerated)",
                n=1,
            )
            sys.stderr.writelines(list(diff)[:80])
            return 1
        return 0

    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)} ({len(rows)} model listings)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
