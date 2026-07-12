# NextBiometrics NB-2020-U (nb1010)

**Status: Merged upstream (libfprint MR !569, merged 2026-07-02)**

Device ID(s): `298d:2020`

This driver is now **merged into upstream libfprint** (git master). It is not in
older released libfprint, so build from libfprint git (or wait for the first
release/distro package that includes it) to get it. Entry kept for people still
on an older libfprint.

## Upstream merge request

- libfprint MR !569 (merged 2026-07-02): https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/569
- Author: Sebastian van de Meer (@Kernel-Error)


## What it does

New nb1010 driver for the NextBiometrics NB-2020-U reader.

## How to use it

The code lives in the merge request, not in this repo. To try it, check out the
MR's source branch of libfprint and build from source (see the
[`27c6:55b4`](../27c6:55b4/) entry for the general libfprint-from-source build
and PAM steps), or follow any instructions in the MR discussion.

```sh
# fetch the MR branch into a libfprint checkout, e.g.
git fetch https://gitlab.freedesktop.org/libfprint/libfprint.git \
  merge-requests/569/head:mr-569
git checkout mr-569
```

## Tested on

Not documented.

## License

Part of libfprint (LGPL-2.1).
