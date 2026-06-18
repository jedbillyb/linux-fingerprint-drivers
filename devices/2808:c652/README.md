# FocalTech FT9362 (match-on-host)

**Status: WIP (unmerged upstream MR)**

Device ID(s): `2808:c652`

This is a driver that has been submitted to the **official libfprint project**
but is **not merged yet**, so it is not in any released libfprint. Tracked here so
people with this sensor can find and build the work in progress.

## Upstream merge request

- libfprint MR !588: https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/588
- Author: Danny Trunk (@dtrunk90)


## What it does

Separate match-on-host driver (64x80 px, ~188 DPI, 16-bit raw over USB bulk). Distinct from the in-tree focaltech_moc match-on-chip driver.

## How to use it

The code lives in the merge request, not in this repo. To try it, check out the
MR's source branch of libfprint and build from source (see the
[`27c6:55b4`](../27c6:55b4/) entry for the general libfprint-from-source build
and PAM steps), or follow any instructions in the MR discussion.

```sh
# fetch the MR branch into a libfprint checkout, e.g.
git fetch https://gitlab.freedesktop.org/libfprint/libfprint.git \
  merge-requests/588/head:mr-588
git checkout mr-588
```

## Tested on

Not documented.

## License

Part of libfprint (LGPL-2.1).
