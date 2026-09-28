# Goodix GF5288 / HTK32 bridge (USB 27c6:5201)

**Status: Working via a community libfprint driver (`goodix5201`), not upstream yet. Enroll, verify and identify through fprintd, tested on one ASUS ZenBook S UX391UA.**

Goodix match-on-host press sensor (108 x 88 pixels, 12 bit) behind Goodix's HT32
USB bridge (USB strings `HTMicroelectronics` / `Goodix Fingerprint Device` /
`HTK32`), running the non-TLS firmware `GF5288_HT_APP_20041`. Found in the ASUS
ZenBook S UX391 series.

## What was broken

Upstream libfprint has no driver for it, so `fprintd-enroll` reports no devices.
The reader enumerates as a CDC ACM modem, so `cdc_acm` binds to it.

Unlike the TLS ("SEC") Goodix readers, it needs no firmware reflash and no PSK:
the firmware is non-TLS and frame data is only obfuscated with Goodix's GEA
stream cipher, using a fixed key found in the Windows driver.

Like the CB2000, each frame covers only about 5.4 x 4.4 mm of the finger. NBIS
finds just 2-3 genuine minutiae per frame, so bozorth3 cannot match.

## What the fix does

[J0UH/goodix-5201-linux](https://github.com/J0UH/goodix-5201-linux) is an in-tree
`FpImageDevice` driver (`goodix5201`) on top of libfprint MR
[!530](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/530)
(SIGFM matching with OpenCV). It:

- detaches `cdc_acm` and talks Goodix's "wrapless" protocol on the bulk endpoints
  of the CDC data interface,
- uploads the 256-byte sensor configuration extracted from the ASUS Windows
  driver on every activation (RAM only, nothing is flashed),
- polls frames against an empty-sensor background, checking the background for
  ridge structure so a finger resting on the sensor is not taken as background,
- matches with SIGFM after 15 enrollment presses. On the author's device,
  same-finger scores were 132 and above, other fingers 0-3, threshold 40.

The repository also has a protocol specification, reverse-engineering notes
(possibly useful for the related `27c6:5301`), a umockdev replay test and an Arch
package.

## Install

This replaces libfprint (it is a patched libfprint, not a TOD module).

- **Arch / Omarchy:** `packaging/arch` in the repository (`makepkg -si`). The
  package also provides `libfprint-git`, so Omarchy's fingerprint setup keeps it.
- **Other distributions:** build the repository's `libfprint` branch as described
  in [docs/BUILD.md](../../docs/BUILD.md). It needs OpenCV (4 or 5) in addition to
  the usual dependencies.

## Tested on

- Arch Linux / Omarchy 4.0.4, fprintd 1.94.5, ASUS ZenBook S UX391UA: enroll 15/15,
  `fprintd-verify` and `sudo` via `pam_fprintd` accepted the enrolled finger, and
  a finger that was not enrolled was rejected.
