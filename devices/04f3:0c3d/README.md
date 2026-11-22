# ELAN press sensor (USB 04f3:0c3d)

**Status: Partial - enroll and verify work with a patched `elanpress` driver and a lower per-device touch threshold; the driver is still an unmerged upstream MR.**

An ELAN press sensor sold as the FeinTech FPS00201 USB fingerprint reader and
found here on an ASUS UX305CA. The USB ID is claimed by upstream's swipe-only
`elan` driver, and libfprint merge request
[!654](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/654)
proposes a dedicated press driver for it.

## What was broken

`04f3:0c3d` is in the `elan` id table, but that driver is swipe-only: it crops
frames, films a resting finger and stitches the result. Enrollment appears to
finish, yet verification always fails with `verify-swipe-too-short` and
`Failed to detect minutiae: No minutiae found`.

Building MR !654 and trying its `elanpress` driver got further - the sensor was
detected and touches were reported - but `fprintd-enroll` still never produced a
profile after about 50 touches. Debug logging showed coverage stuck at 76-86%
while the driver's `ELANPRESS_ACCEPT_COVERAGE` gate is 85%: 104 frames rejected,
0 accepted, no profile written.

## What the fix does

This pad lights a pressed finger much more weakly than the pads the driver's
thresholds were tuned on (a settled press sits about 300-900 above background
instead of 1200+). Three small changes make it work:

1. Move `0x0c3d` from the `elan` id table to `elanpress_id_table`, with an
   `ELANPRESS_0C3D` `driver_data` flag.
2. Select a per-device `ELANPRESS_TOUCH_PIXEL_DELTA_WEAK` of 600 for that flag;
   the other pads keep the default 1200.
3. Move `usb:v04F3p0C3D*` in `data/autosuspend.hwdb` from the generic list to
   the `# Supported by libfprint driver elanpress` section.

The change is also proposed to the driver's source fork as
[filip-rs/libfprint#14](https://github.com/filip-rs/libfprint/pull/14).

## Build and install

`patches/0001-elanpress-driver.patch` adds Filip Spanne's `elanpress` driver to
upstream libfprint; `patches/0002-elanpress-0c3d.patch` adds this sensor on top.
Both apply in that order to upstream libfprint at commit
`6f9479c3d55f847c1b3769f28ceb99227f9858cf` (v1.94.100 + 10). See
`patches/README.md` and [docs/BUILD.md](../../docs/BUILD.md) for the shared
build, install and PAM steps; the only deltas are the two patches and the
enrollment technique below.

A ready-made Arch `PKGBUILD` that applies both patches lives in the source
repository linked in `CREDITS`. **Do not** run
`omarchy setup security fingerprint` afterwards: it reinstalls the unpatched
package and deletes existing prints.

## Enrolling this sensor

The pad needs a **firm, centred press**, not a light touch and not a swipe:

1. Put the right index finger in the middle of the pad.
2. Press firmly and hold for about 1 second.
3. Lift the finger **fully off** the pad and wait about 1 second before the next
   press. Rapid taps are skipped because the driver needs an empty sensor
   between stages.

With the fix, coverage reaches 94-96% and enrollment completes all 24
`enroll-stage-passed` results plus `enroll-completed`. `fprintd-verify` then
returns `verify-match (done)`. The same press technique is needed for
verification; a light touch falls through to the password in PAM.

Progress is not saved until enrollment finishes. To see the 24 stages in a
small terminal window:

```sh
gdbus monitor --system --dest net.reactivated.Fprint |
  grep --line-buffered -E 'enroll-stage-passed|enroll-completed' |
  awk '/stage-passed/{printf "\rStage %d/24", ++n} /completed/{print "\nCompleted!"}'
```

## Tested on

- Omarchy (Arch), libfprint-git `1:1.94.100.r10.g6f9479c-7`, fprintd
  `1.94.5-2`, ASUS UX305CA with a FeinTech FPS00201 (`04f3:0c3d`). Enroll,
  verify, sudo, polkit and lock-screen authentication all reported working on
  2026-11-22. Single reporter, single machine.
- Report and logs: [issue #52](https://github.com/jedbillyb/linux-fingerprint-drivers/issues/52).
