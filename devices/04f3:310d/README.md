# ELAN ELAN7006 (USB 04f3:310d)

**Status: WIP (early draft, unmerged upstream MR)**

Device ID(s): `04f3:310d`

An ELAN ELAN7006 sensor. Upstream libfprint has no working driver for it; a draft
initialisation attempt exists but is **not functional yet** (the author reports
it was tested like ELAN7002 and did not work).

This is an early draft submitted to the **official libfprint project**, tracked
here as a lead for anyone wanting to pick up the reverse-engineering.

## Upstream merge request

- libfprint MR !383: https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/383
- Author: Evgeny Boykov (@boykov)

## What it does

Draft `init` for ELAN7006, modelled on the ELAN7002 path. Does not yet enroll or
verify - treat this as a starting point, not a usable driver.

## How to use it

The code lives in the merge request, not in this repo. To experiment, check out
the MR's source branch of libfprint and build from source (see the
[`27c6:55b4`](../27c6:55b4/) entry for the general libfprint-from-source build).

```sh
git fetch https://gitlab.freedesktop.org/libfprint/libfprint.git \
  merge-requests/383/head:mr-383
git checkout mr-383
```

## Tested on

Not working as of the current draft.

## License

Part of libfprint (LGPL-2.1).
