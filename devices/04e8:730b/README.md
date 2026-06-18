# Samsung 730B (image)

**Status: WIP (unmerged upstream MR)**

Device ID(s): `04e8:730b`

This is a driver that has been submitted to the **official libfprint project**
but is **not merged yet**, so it is not in any released libfprint. Tracked here so
people with this sensor can find and build the work in progress.

## Upstream merge request

- libfprint MR !556: https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/556
- Author: lignah (@lignah)


## What it does

Initial Samsung 730B image driver.

## How to use it

The code lives in the merge request, not in this repo. To try it, check out the
MR's source branch of libfprint and build from source (see the
[`27c6:55b4`](../27c6:55b4/) entry for the general libfprint-from-source build
and PAM steps), or follow any instructions in the MR discussion.

```sh
# fetch the MR branch into a libfprint checkout, e.g.
git fetch https://gitlab.freedesktop.org/libfprint/libfprint.git \
  merge-requests/556/head:mr-556
git checkout mr-556
```

## Tested on

Not documented.

## License

Part of libfprint (LGPL-2.1).
