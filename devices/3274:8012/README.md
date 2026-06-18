# Microarray match-on-chip (PID 8012)

**Status: WIP (unmerged upstream MR, Draft)**

Device ID(s): `3274:8012`

This is a driver that has been submitted to the **official libfprint project**
but is **not merged yet**, so it is not in any released libfprint. Tracked here so
people with this sensor can find and build the work in progress.

## Upstream merge request

- libfprint MR !492: https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/492
- Author: wsj (@FarmerCode)
- Marked **Draft** by the author.

## What it does

Adds PID 8012 to a Microarray match-on-chip (mafpmoc) driver. Closes upstream issue #659.

## How to use it

The code lives in the merge request, not in this repo. To try it, check out the
MR's source branch of libfprint and build from source (see the
[`27c6:55b4`](../27c6:55b4/) entry for the general libfprint-from-source build
and PAM steps), or follow any instructions in the MR discussion.

```sh
# fetch the MR branch into a libfprint checkout, e.g.
git fetch https://gitlab.freedesktop.org/libfprint/libfprint.git \
  merge-requests/492/head:mr-492
git checkout mr-492
```

## Tested on

Not documented.

## License

Part of libfprint (LGPL-2.1).
