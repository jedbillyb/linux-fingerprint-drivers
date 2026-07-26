# ELAN image sensors - poor upstream behaviour (USB 04f3:0c28 and the 0c0x/0c1x/0c2x family)

**Status: Claimed upstream, but frequently unusable. Two open MRs improve it.**

The in-tree `elan` driver claims a long list of ELAN image sensors
(`04f3:0c01` through `04f3:0c4x`, including `04f3:0c28`). Being on libfprint's
supported list is misleading here: on many of these readers enrollment fails at
every second capture, or never completes at all.

If your ELAN reader is *recognised* by libfprint but you cannot finish an
enrollment, this entry is for you. If it is not recognised at all, you want a
different entry: see the [ELAN entries](../) for `0c4c`, `0c6c`, `0c8e`, `0c9c`,
`310d`.

## What is broken

Reported by the MR authors and matching a long tail of user bug reports:

- Too few calibration loops, so every second capture fails.
- Result code `0xaf` from `CAPTURE_READ_DATA` is unhandled, and it occurs often.
- `bz3_threshold` is too high for these low-resolution, low-quality images.
- Captures are treated as swipe images to give NBIS enough pixels, which fits the
  hardware poorly - these are press sensors.

## What the fixes do

**libfprint MR [!217](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/217)**
("elan: Add support for touch devices", Piotr Piastucki / @ppiastucki), based in
part on iafilatov's `elan-touch` branch: more calibration loops, handling for
`0xaf`, a lower `bz3_threshold`, image resize plus a sharpening convolution to
roughly double extracted minutiae.

**libfprint MR [!530](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/530)**
("add sigfm algorithm implementation (rebased and enabled Elan sensors)", @Tooniis,
continuing @418's work): brings the OpenCV-based **sigfm** matcher into libfprint
and switches ELAN sensors to it, so they can be used as the press sensors they
are instead of being faked as swipe devices.

The two are independent; !530 is the more fundamental change and is actively
rebased on master.

## How to try them

```sh
git clone https://gitlab.freedesktop.org/libfprint/libfprint.git
cd libfprint
git fetch origin merge-requests/530/head:mr-530   # or 217
git checkout mr-530
```

!530 needs **OpenCV** (and doctest for its tests) on top of the usual build
dependencies. Then build per [docs/BUILD.md](../../docs/BUILD.md).

## Tested on

- MR !217: the author's `04f3:0c28` reader, where stock libfprint could not
  complete an enrollment.
- MR !530: the author's ELAN sensors, using sigfm in press mode.
- If you have any `04f3:0c0x`-`0c4x` reader, a before/after report is valuable -
  this family is large and under-reported.

## License

Part of libfprint (LGPL-2.1).
