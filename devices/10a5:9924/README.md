# FPC match-on-host (USB 10a5:9924)

**Status: WIP (unmerged upstream MR)**

Device ID(s): `10a5:9924`

An FPC (Fingerprint Cards) match-on-host sensor handled by the `fpcmoc` driver.
Seen on Honor laptops. Upstream `fpcmoc` does not yet list this product ID.

This is a driver change submitted to the **official libfprint project** but
**not merged yet**, tracked here so people with this sensor can find and build
the work in progress.

## Upstream merge request

- libfprint MR !611: https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/611
- Author: zeno (@Zeno-sole)

## What it does

Adds `10a5:9924` to the `fpcmoc` driver table and to the USB autosuspend hwdb.
Also adds fallback handling for a non-standard identity format used by some FPC
sensors (e.g. `FPC L:2407`) during verify, where the sensor reports a match with
zero identity fields.

Protocol reference / origin fork:
https://github.com/reackcjq/honor-fpc-fingerprint-linux

## Related entries

- [`10a5:9800`](../10a5:9800/) - another FPC match-on-host (`fpcmoh`) sensor,
  already working.
- [`10a5:9200`](../10a5:9200/) - FPC1022 Disum (`fpcmoh`), WIP.

## How to use it

The code lives in the merge request, not in this repo. To try it, check out the
MR's source branch of libfprint and build from source (see the
[`27c6:55b4`](../27c6:55b4/) entry for the general libfprint-from-source build
and PAM steps).

```sh
git fetch https://gitlab.freedesktop.org/libfprint/libfprint.git \
  merge-requests/611/head:mr-611
git checkout mr-611
```

## Tested on

See the MR discussion.

## License

Part of libfprint (LGPL-2.1).
