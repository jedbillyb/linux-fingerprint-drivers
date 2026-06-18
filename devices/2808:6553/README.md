# FocalTech FT9365 ESS (focaltech_moc)

**Status: WIP (unmerged upstream MR)**

Device ID(s): `2808:6553`

This is a driver that has been submitted to the **official libfprint project**
but is **not merged yet**, so it is not in any released libfprint. Tracked here so
people with this sensor can find and build the work in progress.

## Upstream merge request

- libfprint MR !554: https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/554
- Author: Sid1803 (@sid1803)


## What it does

Found in the Samsung Galaxy Book 4. Adds the ID to focaltech_moc and accepts status code 0x09 (which the in-tree driver wrongly treated as an error) so enroll completes.

## How to use it

The code lives in the merge request, not in this repo. To try it, check out the
MR's source branch of libfprint and build from source (see the
[`27c6:55b4`](../27c6:55b4/) entry for the general libfprint-from-source build
and PAM steps), or follow any instructions in the MR discussion.

```sh
# fetch the MR branch into a libfprint checkout, e.g.
git fetch https://gitlab.freedesktop.org/libfprint/libfprint.git \
  merge-requests/554/head:mr-554
git checkout mr-554
```

## Tested on

Verified on Arch Linux (kernel 6.17.9).

## License

Part of libfprint (LGPL-2.1).
