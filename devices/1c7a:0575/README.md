# EgisTec EGIS0575 (swipe)

**Status: WIP (unmerged upstream MR)**

Device ID(s): `1c7a:0575`

This is a driver that has been submitted to the **official libfprint project**
but is **not merged yet**, so it is not in any released libfprint. Tracked here so
people with this sensor can find and build the work in progress.

## Upstream merge request

- **libfprint MR !695 (current):** https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/695
  - Author: gpro. Opened 2026-11-12 to continue !357, which had not changed
    since March 2023. Rebased on current master, squashed as !357's reviewers
    asked, plus two fixes for problems reported in the !357 discussion. The
    author uses it daily on an Acer Swift 3 SF314-43.
- libfprint MR !357 (original, stalled): https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/357
- Author: topni1 (@topni1)


## What it does

New egis0575 driver, implemented as a swipe sensor; needs a long, steady swipe for good results.

## How to use it

The code lives in the merge request, not in this repo. To try it, check out the
MR's source branch of libfprint and build from source (see
[docs/BUILD.md](../../docs/BUILD.md) for the shared build, install, PAM and
troubleshooting steps), or follow any instructions in the MR discussion.

```sh
# fetch the MR branch into a libfprint checkout, e.g.
git fetch https://gitlab.freedesktop.org/libfprint/libfprint.git \
  merge-requests/695/head:mr-695
git checkout mr-695
```

## Tested on

- Acer Swift 3 SF314-43 (reported by the author of !695, daily use)

## License

Part of libfprint (LGPL-2.1).

## Reverse-engineering notes

[Animeshz/EgisTec-EH575](https://github.com/Animeshz/EgisTec-EH575) collects
protocol findings and a libfprint patch for this sensor (39 stars, last touched
2022). It carries **no license file**, so nothing from it is mirrored here and it
cannot be contributed upstream as-is, but the findings are a useful reference if
you pick this driver up.
