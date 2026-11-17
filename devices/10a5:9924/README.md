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
- libfprint MR !666 (follow-up): https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/666
  - Author: codethinki. Picks up !611 on an HONOR MagicBook Pro 14 (2025,
    FMB-P). The sensor re-enumerates when `fpc_dev_open()` resets it, which
    left the driver with a stale handle and broke enrollment; !666 skips the
    reset for this PID and drops !611's identity fallback, so verify still
    checks which print matched.

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
MR's source branch of libfprint and build from source (see
[docs/BUILD.md](../../docs/BUILD.md) for the shared build, install and PAM steps).

```sh
git fetch https://gitlab.freedesktop.org/libfprint/libfprint.git \
  merge-requests/611/head:mr-611
git checkout mr-611
```

## Tested on

See the MR discussion.

## License

Part of libfprint (LGPL-2.1).
