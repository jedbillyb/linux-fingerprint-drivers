# FocalTech FT9348 - standalone capture + vendor matcher (USB 2808:9348)

**Status: Works (sudo, GNOME unlock) via a standalone GPL-2.0 tool plus FocalTech's proprietary matcher. Not a libfprint driver.**

> **This entry hosts no code.** The working route is
> [narkomart/focaltech-ft9348-linux](https://github.com/narkomart/focaltech-ft9348-linux)
> (GPL-2.0, so it cannot be mirrored into this LGPL-2.1 hub), and its matching step
> needs FocalTech's **closed-source** libfprint `.so`, which that project does not
> redistribute either. Catalogued so owners of this sensor can find a route; read
> the [caveats](#caveats) before putting it in your authentication path.

Small (64x80 px, about 3x4 mm) sensor built into the **power button**; internal chip
id `0x9362`. Seen in a DIGMA Pro Magnus M laptop.

## What was broken

Upstream libfprint has no driver for `2808:9348`. The FocalTech work that exists
targets other parts and does not fit this one:

- the FT9201 drivers (see [`2808:9338`](../2808:9338/)) and the vendor `ft9366`
  path talk to the chip with bulk commands; on `9348` those time out. This chip is
  driven by **USB control transfers**: register read = `bmRequestType 0xC0,
  bRequest=<reg>`, write = `0x40`; finger present = reg `0x43`; one frame = 5120
  bytes bulk-IN on EP `0x83` after three register writes. Full protocol in the
  project's `docs/PROTOCOL.md`.
- with the image in hand, libfprint's generic NBIS matcher scored 0 on this tiny
  sensor. FocalTech's own matcher is a CNN (GhostNet), not minutiae.

## The route

`ftbio` (the project's standalone binary) captures frames over libusb with the
control-transfer protocol, and matches them by `dlopen`ing FocalTech's proprietary
libfprint `.so` and calling its internal `focal_*` algorithm functions, resolved by
symbol name. Login is wired through `pam_exec` for `sudo` and `gdm-password`
(GNOME lock screen); the password stays as fallback (`sufficient`).

The `.so` comes from FocalTech's own Linux driver packages, which the user downloads;
the project's `get-matcher.sh` checks that a supplied file has the needed symbols
before installing it. Follow the project README; the generic steps in
[docs/BUILD.md](../../docs/BUILD.md) do not apply.

Enroll with many touches (the tool asks for 30, shifting the finger each time):
on this sensor a 12-touch template recognised new touches only about every other
time. The template self-learns after each successful match.

## Caveats

- **Proprietary blob in the auth path.** Matching runs closed FocalTech code as
  root. Not auditable.
- **Not libfprint/fprintd.** fprintd must be stopped/masked (it would grab the
  device); GNOME Settings does not see the fingerprint; the GDM *login* greeter may
  not run `pam_exec` before the password is typed - lock-screen unlock works.
- Unlocking by fingerprint leaves the GNOME keyring locked (normal for biometrics).
- One finger per user so far.
- If you want this sensor upstream, it needs an LGPL-2.1 libfprint driver with an
  open matcher; the capture protocol is documented and could be reused.

## Tested on

- DIGMA Pro Magnus M (DN16R7), Ubuntu 24.04, kernel 6.8: enroll, verify, `sudo`,
  GNOME lock screen. After a 30-touch enrollment, 9 of 9 `sudo` attempts matched,
  usually on the first or second touch; a different finger was rejected in all
  tests.

## License note

The tool is GPL-2.0; the matcher is proprietary FocalTech code. Catalogued as a
pointer only; no code from either is present in this repo.
