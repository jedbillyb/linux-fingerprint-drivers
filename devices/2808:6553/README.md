# FocalTech FT9365 ESS (focaltech_moc)

**Status: Merged upstream (libfprint MR !554, merged 2026-06-18)**

Device ID(s): `2808:6553`

This driver is now **merged into upstream libfprint** (git master). It is not in
older released libfprint, so build from libfprint git (or wait for the first
release/distro package that includes it) to get it. Entry kept for people still
on an older libfprint.

## Upstream merge request

- libfprint MR !554 (merged 2026-06-18): https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/554
- Author: Sid1803 (@sid1803)


## What it does

Found in the Samsung Galaxy Book 4. Adds the ID to focaltech_moc and accepts status code 0x09 (which the in-tree driver wrongly treated as an error) so enroll completes.

## Caveat on dual-function FT9201 modules

> **This driver is not the right target if your module also exposes `2808:93a9`.**

Some FocalTech modules present **two** USB functions from one physical part:
`2808:93a9` (the FT9201 image sensor, USB class 255) and `2808:6553` (the FT9365
secure-storage companion, USB class 220 / Diagnostic). On that hardware,
`focaltech_moc` binds `6553` and everything *looks* correct - `fprintd-list`
shows the device, `enroll_times` comes back from the chip, `scan-type = press`,
and `EnrollStart` is accepted - but it never captures, because there is no
sensor on that function. A reported `usbmon` trace over a 120 s enroll with the
sensor being touched continuously shows the finger poll answered with one
identical response 2249 times, with no variation; enroll then sits in
`MOC_IDENTIFY` until it cancels. **No error is surfaced**, so it presents as a
broken sensor rather than as the wrong function.

Capture on those modules has to go through `93a9` - see
[`devices/2808:9338`](../2808:9338/). Standalone `6553` devices (such as the
Galaxy Book 4 hardware this MR was written and verified against) are unaffected;
this is a note about which function to bind, not a defect in !554.

Reported in [issue #2](https://github.com/jedbillyb/linux-fingerprint-drivers/issues/2)
by @NBN-N3 (Kali, kernel 6.17), on a single module - corroboration from other
dual-function hardware is welcome.

## How to use it

The code lives in the merge request, not in this repo. To try it, check out the
MR's source branch of libfprint and build from source (see
[docs/BUILD.md](../../docs/BUILD.md) for the shared build, install, PAM and
troubleshooting steps), or follow any instructions in the MR discussion.

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
