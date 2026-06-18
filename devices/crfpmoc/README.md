# Chromium OS EC FPMCU (match-on-chip)

**Status: WIP (unmerged upstream MR)**

Device ID(s): `cros_ec (not USB)`

This is a driver that has been submitted to the **official libfprint project**
but is **not merged yet**, so it is not in any released libfprint. Tracked here so
people with this sensor can find and build the work in progress.

## Upstream merge request

- libfprint MR !512: https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/512
- Author: Xelef2000 (@Xelef2000)


## What it does

Match-on-chip driver for the Chromium OS EC fingerprint MCU (FPMCU) found in Chromebooks. Not a USB device; it speaks the cros_ec protocol. Continues earlier MR !493 by Abhinav Baid.

## How to use it

The code lives in the merge request, not in this repo. To try it, check out the
MR's source branch of libfprint and build from source (see the
[`27c6:55b4`](../27c6:55b4/) entry for the general libfprint-from-source build
and PAM steps), or follow any instructions in the MR discussion.

```sh
# fetch the MR branch into a libfprint checkout, e.g.
git fetch https://gitlab.freedesktop.org/libfprint/libfprint.git \
  merge-requests/512/head:mr-512
git checkout mr-512
```

## Tested on

Not documented.

## License

Part of libfprint (LGPL-2.1).
