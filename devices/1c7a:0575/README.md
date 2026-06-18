# EgisTec EGIS0575 (swipe)

**Status: WIP (unmerged upstream MR)**

Device ID(s): `1c7a:0575`

This is a driver that has been submitted to the **official libfprint project**
but is **not merged yet**, so it is not in any released libfprint. Tracked here so
people with this sensor can find and build the work in progress.

## Upstream merge request

- libfprint MR !357: https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/357
- Author: topni1 (@topni1)


## What it does

New egis0575 driver, implemented as a swipe sensor; needs a long, steady swipe for good results. (USB ID inferred from the EgisTec vendor 1c7a and driver name; confirm against the MR.)

## How to use it

The code lives in the merge request, not in this repo. To try it, check out the
MR's source branch of libfprint and build from source (see the
[`27c6:55b4`](../27c6:55b4/) entry for the general libfprint-from-source build
and PAM steps), or follow any instructions in the MR discussion.

```sh
# fetch the MR branch into a libfprint checkout, e.g.
git fetch https://gitlab.freedesktop.org/libfprint/libfprint.git \
  merge-requests/357/head:mr-357
git checkout mr-357
```

## Tested on

Not documented.

## License

Part of libfprint (LGPL-2.1).
