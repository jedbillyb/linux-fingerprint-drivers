# ELAN ARM-M4 (0c9c)

**Status: Merged upstream (libfprint MR !568, merged 2026-06-18)**

Device ID(s): `04f3:0c9c`

This driver is now **merged into upstream libfprint** (git master). It is not in
older released libfprint, so build from libfprint git (or wait for the first
release/distro package that includes it) to get it. Entry kept for people still
on an older libfprint.

## Upstream merge request

- libfprint MR !568 (merged 2026-06-18): https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/568
- Author: Petapton (@Petapton)


## What it does

Adds support for the Elan 04f3:0c9c (ELAN:ARM-M4) sensor.

## How to use it

The code lives in the merge request, not in this repo. To try it, check out the
MR's source branch of libfprint and build from source (see the
[`27c6:55b4`](../27c6:55b4/) entry for the general libfprint-from-source build
and PAM steps), or follow any instructions in the MR discussion.

```sh
# fetch the MR branch into a libfprint checkout, e.g.
git fetch https://gitlab.freedesktop.org/libfprint/libfprint.git \
  merge-requests/568/head:mr-568
git checkout mr-568
```

## Tested on

Not documented.

## License

Part of libfprint (LGPL-2.1).
