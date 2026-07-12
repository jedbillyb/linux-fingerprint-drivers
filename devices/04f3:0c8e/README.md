# ELAN elanmoc2 (0c8e)

**Status: Stale (upstream MR !560 was closed without merging)**

Device ID(s): `04f3:0c8e`

A driver was submitted to the **official libfprint project** but the merge
request was **closed without being merged**, so there is no maintained upstream
work for this sensor right now. The MR branch below still exists and may be a
usable starting point, but it is unmaintained - treat this as a lead for someone
to pick up rather than a ready driver.

## Upstream merge request

- libfprint MR !560 (**closed, not merged**): https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/560
- Author: REYSEIL FULLBRYGER (@reyseilfullbryger)


## What it does

Adds the 04f3:0c8e sensor to an elanmoc2 driver.

## How to use it

The code lives in the merge request, not in this repo. To try it, check out the
MR's source branch of libfprint and build from source (see the
[`27c6:55b4`](../27c6:55b4/) entry for the general libfprint-from-source build
and PAM steps), or follow any instructions in the MR discussion.

```sh
# fetch the MR branch into a libfprint checkout, e.g.
git fetch https://gitlab.freedesktop.org/libfprint/libfprint.git \
  merge-requests/560/head:mr-560
git checkout mr-560
```

## Tested on

Not documented.

## License

Part of libfprint (LGPL-2.1).
