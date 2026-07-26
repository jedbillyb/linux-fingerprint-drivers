# Microarray MAFP8800 (SPI)

**Status: WIP (unmerged upstream MR)**

Device ID(s): `ACPI HID MAFP8800 (SPI, not USB)`

This is a driver that has been submitted to the **official libfprint project**
but is **not merged yet**, so it is not in any released libfprint. Tracked here so
people with this sensor can find and build the work in progress.

## Upstream merge request

- libfprint MR !580: https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/580
- Author: Mark (@IngeniousIdiocy)


## What it does

SPI fingerprint sensor exposed via ACPI HID MAFP8800 over spidev (GPD MicroPC 2, Chuwi MiniBook X). Subclasses FpDevice with its own SIFT-WHT + RANSAC matching because the 36x160 captures yield too few minutiae for bozorth3.

## How to use it

The code lives in the merge request, not in this repo. To try it, check out the
MR's source branch of libfprint and build from source (see
[docs/BUILD.md](../../docs/BUILD.md) for the shared build, install, PAM and
troubleshooting steps), or follow any instructions in the MR discussion.

```sh
# fetch the MR branch into a libfprint checkout, e.g.
git fetch https://gitlab.freedesktop.org/libfprint/libfprint.git \
  merge-requests/580/head:mr-580
git checkout mr-580
```

## Tested on

Not documented.

## License

Part of libfprint (LGPL-2.1).
