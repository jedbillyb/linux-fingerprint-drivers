# Validity/Synaptics VCSFW 0x969 (USB 138a:00ab)

**Status: WIP (unmerged upstream MR) - hardware-validated by the MR author.**

Device ID(s): `138a:00ab`

A Synaptics/Validity **VCSFW** sensor: TLS-paired, match-on-chip, with enroll,
matching and template storage all happening on the sensor. libfprint has no
driver for these today, so they do not work under current fprintd at all.

## Hardware

HP ZBook Studio x360 G5, and other models carrying the same sensor.

## Upstream merge request

- libfprint MR !626: https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/626
- Author: Gary T. Giesen (@ggiesen)

This continues @lewohart's [!579](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/579),
which has been inactive since April 2026; !579's driver is preserved inside it as
a single commit with authorship intact. !626 is the branch to build.

## What it does

Implements the full `FpDevice` surface (open/close, enroll, verify, identify,
list, delete, clear-storage) and handles the on-chip TLS session, host pairing,
calibration and the flash template database in-driver. Each device loads a
per-device data package at runtime; see the MR description for details.

The MR author reports daily-driver use, including PAM screen unlock.

`138a:00ab` ships with either 0x969 or 0xd51 silicon depending on the model. The
driver keys its silicon-specific handling off the sensor type the device reports,
not off the USB ID, so both variants are handled by the same entry.

## How to use it

The code lives in the merge request, not in this repo:

```sh
git clone https://gitlab.freedesktop.org/libfprint/libfprint.git
cd libfprint
git fetch origin merge-requests/626/head:mr-626
git checkout mr-626
```

Then build and install per [docs/BUILD.md](../../docs/BUILD.md).

## Related entries

- [`138a:0097`](../138a:0097/) - the wider VCSFW family entry, covering
  `138a:0090`, `138a:0097`, `138a:009d` and `06cb:009a`.
- [`06cb:009a`](../06cb:009a/) - python-validity, the established userspace route
  for part of this family.

## Pairing caveat

These sensors store host pairing data on-chip, so pairing with Linux can
invalidate a Windows Hello pairing. Dual-booters should expect to re-enroll on
one side.

## Tested on

- Confirmed working on the hardware above by the MR author (Linux Mint).
- More reports welcome, especially distro + libfprint version.

## License

Part of libfprint (LGPL-2.1).
