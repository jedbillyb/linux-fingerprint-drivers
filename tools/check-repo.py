#!/usr/bin/env python3
"""Consistency checks for this repo. Run with no arguments:

    python3 tools/check-repo.py

Exits non-zero and prints one line per problem. CI runs this on every PR, so a
new device entry that is missing a file, is not listed in the README, or has a
broken link fails the build instead of rotting quietly.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEVICES = REPO / "devices"

# Entries for sensors that are not on USB, so they have no vendor:product ID.
NON_USB_ENTRIES = {"broadcom-controlvault3", "crfpmoc", "mafp8800"}

USB_ID = re.compile(r"^[0-9a-f]{4}:[0-9a-f]{4}$")
ANY_USB_ID = re.compile(r"\b[0-9a-f]{4}:[0-9a-f]{4}\b")
MD_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")

problems: list[str] = []


def fail(where: Path | str, msg: str) -> None:
    rel = Path(where).relative_to(REPO) if isinstance(where, Path) else where
    problems.append(f"{rel}: {msg}")


def markdown_files() -> list[Path]:
    return sorted(p for p in REPO.rglob("*.md") if ".git" not in p.parts)


def check_device_entries(readme: str) -> None:
    entries = sorted(p for p in DEVICES.iterdir() if p.is_dir())
    if not entries:
        fail(DEVICES, "no device entries found")

    for entry in entries:
        name = entry.name
        if not USB_ID.match(name) and name not in NON_USB_ENTRIES:
            fail(
                entry,
                "directory name must be a lowercase 'vendor:product' USB ID "
                "(or be added to NON_USB_ENTRIES in tools/check-repo.py)",
            )

        for required in ("README.md", "CREDITS"):
            path = entry / required
            if not path.is_file():
                fail(entry, f"missing required file {required}")
            elif not path.read_text().strip():
                fail(path, "is empty")

        patches = entry / "patches"
        if not patches.is_dir():
            fail(entry, "missing patches/ directory (see CONTRIBUTING.md)")
        else:
            check_patches(patches)

        if name not in readme:
            fail(
                entry,
                "not listed in the top-level README.md - add a table row so "
                "people can find it",
            )

        check_device_readme(entry / "README.md")


def check_patches(patches: Path) -> None:
    index = patches / "README.md"
    if not index.is_file():
        fail(patches, "missing README.md stating the libfprint base commit")

    series = sorted(patches.glob("*.patch")) + sorted(patches.glob("*.diff"))
    for patch in series:
        head = patch.read_text(errors="replace").lstrip()
        if not (head.startswith("From ") or head.startswith("diff ")):
            fail(patch, "does not look like a git patch/diff")

    if series and index.is_file():
        text = index.read_text()
        if not re.search(r"\b[0-9a-f]{7,40}\b", text):
            fail(
                index,
                "patch files present but no base commit hash documented - "
                "state the libfprint commit the series applies to",
            )


def check_device_readme(readme: Path) -> None:
    if not readme.is_file():
        return
    text = readme.read_text()
    if not text.lstrip().startswith("# "):
        fail(readme, "should start with a '# <chip> (<USB ID>)' heading")
    if "## Tested on" not in text:
        fail(readme, "missing a '## Tested on' section")
    if "**Status:" not in text:
        fail(
            readme,
            "missing a '**Status: ...**' line near the top - tools/detect.sh "
            "reports it to users",
        )


def check_links() -> None:
    for md in markdown_files():
        for target in MD_LINK.findall(md.read_text()):
            target = target.strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path, _, _anchor = target.partition("#")
            if not path:
                continue
            resolved = (md.parent / path).resolve()
            if not resolved.exists():
                fail(md, f"broken relative link: {target}")


def check_no_contradictions(readme: str) -> None:
    gap_map = REPO / "docs" / "unsupported-devices.md"
    if not gap_map.is_file():
        fail("docs/unsupported-devices.md", "missing")
        return

    # Only the table rows are claims of "no known fix"; the prose above the
    # table deliberately cross-references entries that do have work.
    rows = [
        line for line in gap_map.read_text().splitlines() if line.startswith("| [")
    ]
    listed = set(ANY_USB_ID.findall("\n".join(rows)))
    have_entry = {p.name for p in DEVICES.iterdir() if p.is_dir()}
    for device_id in sorted(listed & have_entry):
        fail(
            gap_map,
            f"{device_id} is listed as having no known fix but has an entry in "
            f"devices/{device_id}/ - remove the gap-map row",
        )

    if "docs/unsupported-devices.md" not in readme:
        fail("README.md", "does not link to docs/unsupported-devices.md")


def check_models() -> None:
    """MODELS files feed docs/laptops.md and the per-page titles on the site.

    They are optional (plenty of sensors have no reported machine yet), but a
    malformed one silently distorts the laptop index, so the format is checked.
    """
    for entry in sorted(p for p in DEVICES.iterdir() if p.is_dir()):
        models = entry / "MODELS"
        if not models.is_file():
            continue
        lines = [ln.rstrip() for ln in models.read_text().splitlines()]
        useful = [ln.strip() for ln in lines if ln.strip() and not ln.startswith("#")]
        if not useful:
            fail(models, "exists but lists no models; delete it instead")
        if len(useful) != len(set(useful)):
            fail(models, "lists the same model twice")
        for line in useful:
            if len(line) > 80:
                fail(models, f"model name looks like prose, not a model: {line[:50]}...")
            if line.startswith(("-", "*", "|")):
                fail(models, f"one plain model per line, no list markup: {line[:50]}")


def check_laptop_index() -> None:
    index = REPO / "docs" / "laptops.md"
    if not index.is_file():
        fail("docs/laptops.md", "missing; run python3 tools/gen-laptop-index.py")
        return
    if "gen-laptop-index.py" not in index.read_text():
        fail(
            "docs/laptops.md",
            "is missing its generated-file marker; it must not be hand-edited",
        )


def check_tools_executable() -> None:
    for script in sorted((REPO / "tools").glob("*.sh")):
        if not script.stat().st_mode & 0o111:
            fail(script, "is not executable (chmod +x)")


def main() -> int:
    readme_path = REPO / "README.md"
    if not readme_path.is_file():
        print("README.md: missing", file=sys.stderr)
        return 1
    readme = readme_path.read_text()

    check_device_entries(readme)
    check_links()
    check_no_contradictions(readme)
    check_models()
    check_laptop_index()
    check_tools_executable()

    entry_count = len([p for p in DEVICES.iterdir() if p.is_dir()])
    if problems:
        print(f"{len(problems)} problem(s) found:\n")
        for problem in problems:
            print(f"  {problem}")
        return 1

    print(f"OK: {entry_count} device entries, all links and files consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
