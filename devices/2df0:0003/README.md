# CanvasBio CB2000 (USB 2df0:0003)

**Status: Working via community drivers, none of them upstream; the sibling ID `2df0:0007` is not covered by any of them and stalls on contact.**

CanvasBio CB2000, the fingerprint reader in the Samsung Galaxy Book2 360 and
Book3 360 generation. Upstream libfprint has never supported it and there is no
merge request for `2df0` in any state, but four independent people have
reverse-engineered it from the Samsung Windows driver, and at least two report
daily use for login and `sudo`.

## What was broken

The sensor is unknown to stock libfprint, so nothing binds to it and
`fprintd-enroll` reports no devices.

Worse, it does not fit libfprint's normal image path even once you can talk to
it. The CB2000 delivers an 80x64 greyscale image covering roughly 5x4 mm of
fingertip. NBIS/bozorth3 wants somewhere around 20 minutiae to match; on frames
this small it typically finds 0 to 3. Neither adjusting `ppmm` nor upscaling
helps, because the minutiae are not in the frame to begin with. Every working
driver below therefore derives from `FpDevice` rather than `FpImageDevice` and
brings its own matcher, building a template from many frames instead of one.

## The drivers

None of these is upstream, none is packaged by a distro, and all of them
replace or extend your libfprint. Read the source before installing.

| Project | Approach | Licence | Notes |
|---------|----------|---------|-------|
| [kpagnussat/canvasbio-cb2000](https://github.com/kpagnussat/canvasbio-cb2000) | SIGFM feature matching, multi-capture mosaic template | LGPL-2.1 | Most actively developed. `R2.5` snapshot, 15 enroll stages, requires OpenCV, disables libfprint's virtual thermal shutdown for this device. Also published as a [single-file snippet](https://gitlab.com/-/snippets/4931207) |
| [LennartArnholdt/libfprint-tod-cb2000](https://github.com/LennartArnholdt/libfprint-tod-cb2000) | SIFT feature matching, 30-frame template | LGPL-2.1-or-later AND MIT | Reports ~83% single-touch genuine acceptance and 0 false accepts in 1080 comparisons, measured across separate sessions on one device. PAM setup documented |
| [latex/canvasbio-cb2000-linux-driver](https://github.com/latex/canvasbio-cb2000-linux-driver) | Standalone driver plus CLI tooling (`cb2000_demo`, `fpsudo`) | MIT | Ships an `install.sh`. Developed on a Book3 360 (730QFG) |
| [rfocosi/libfprint](https://github.com/rfocosi/libfprint) | libfprint fork carrying a CB2000 driver | none stated | Whole-library fork rather than a patch |
| [vgperess/libfprint-canvasbio-cb2000](https://github.com/vgperess/libfprint-canvasbio-cb2000) | - | none stated | Earliest of the set, quiet since 2025 |

**On licensing:** this repo hosts none of the above, it points at them. The MIT
and unlicensed ones are noted so you can make your own call before mixing code
into an LGPL-2.1 library.

## Do not use these on 2df0:0007

`2df0:0007` is a different part in the same family, reported in the Samsung
Galaxy Book5 360. It is **not** supported by any driver here, and at least one
of them lists the ID anyway.

kpagnussat's `id_table` carries both `0x0003` and `0x0007`, but nothing else in
that driver looks at which product it is talking to, so a `:0007` binds and is
then driven with a command set traced entirely off `:0003` hardware. The
observed result is an immediate stall on the first vendor control request of
the wake sequence, followed by an endless USB reset and re-init loop:

```text
[activation_wake] cmd 1/10 CTRL_OUT req=0xdb value=0x0001 index=1
Command transfer failed: endpoint stalled or request not supported
```

Reverse-engineering notes in
[myso-kr/samsung-galaxy-book-fingerprint-sensor-device-730b](https://github.com/myso-kr/samsung-galaxy-book-fingerprint-sensor-device-730b/blob/main/docs/reverse-engineering/driver-analysis.md)
describe `2df0:0007` as match-on-chip with SDCP and TLS, off a Realtek UMDF
driver, against the plain unencrypted image sensor that `:0003` is known to be.
That is third-party and unverified, but it is consistent with a device
rejecting a bare vendor request outright.

If you have a `:0007`, the useful contribution is a full `lsusb -v` dump,
especially the BOS descriptor, and a Windows-side USB capture if you can get
one. Tracked in
[issue #17](https://github.com/jedbillyb/linux-fingerprint-drivers/issues/17).

## Build and install

Each project ships its own instructions and they differ, so follow the one you
pick. [docs/BUILD.md](../../docs/BUILD.md) covers the shared shape: building
libfprint from source, installing over your distro's copy, PAM setup and
troubleshooting. Sensor-specific deltas:

- kpagnussat's `R2.5` needs OpenCV present at build and run time, and enrolls
  in 15 stages rather than the usual 5, so expect a longer enrollment.
- Templates are multi-frame for every driver here. Re-enroll after switching
  drivers rather than expecting old prints to carry over.
- Expect to re-touch on some verifications. A 5x4 mm capture area means two
  presses can share almost no skin, so allow three PAM attempts.

> These replace a core system library. Keep a way to reinstall your distro's
> stock libfprint, which will also silently undo the driver on the next update.

## Tested on

- Samsung Galaxy Book3 360, daily use for login and `sudo`, per
  LennartArnholdt's and kpagnussat's own reports. Both note their accuracy
  figures come from one person on one device.
- Samsung Galaxy Book2 360, reported as working but stricter, sometimes needing
  threshold tuning.
- `2df0:0003` also recorded on a Samsung 730QED by a linuxhw hardware probe
  under Fedora 38.
