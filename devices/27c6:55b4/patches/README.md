# Patches for Goodix GF3268 (27c6:55b4)

These are `git format-patch` exports of the full `goodix-55b4-fixes` branch (see
`../CREDITS`), one patch per commit, in order. Applied on top of the base commit
below they reproduce the branch tip exactly (verified with `git am`).

## Base

- **libfprint version:** 1.94.6 (`meson.build` `version: '1.94.6'`)
- **Base commit:** `d1ca62a` - "Do not cancel read because in gnome lock screen
  after one unsuccessful attempt it stops working" (by Alireza S.N), the last
  upstream commit on the goodixtls fork before this fix series.

If you are building from the patched fork directly you do **not** need these -
just build the `goodix-55b4-fixes` branch as described in `../README.md`. The
patches are here so the fix can be reproduced against a plain checkout of that
goodixtls base.

## Series

Apply in numeric order:

1. `0001` - sigfm: make sigfm-tests conditional on doctest (build fix)
2. `0002` - accept the `GF3268_RTSEC_APP` firmware family so the device is recognised
3. `0003` - (re)provision the PSK instead of only checking it
4. `0004` - fix the preset PSK write framing
5. `0005` - enable PSK ciphers for the sensor TLS handshake
6. `0006` - tighten the sigfm matching thresholds
7. `0007` - keep device + TLS session warm across verify retries
8. `0008` - README: document the fork (build, enroll, tuning)
9. `0009` - revert 0007 (warm-TLS session went stale after idle)

Note: `0007` and `0009` cancel out (the warm-TLS experiment was reverted), and
`0008` is the fork's own README. They are kept so the series reproduces the
branch faithfully; the actual driver fix is patches `0002`-`0006`.

## How to apply

```sh
# from inside a libfprint checkout at the base commit d1ca62a
git am /path/to/devices/27c6:55b4/patches/0*.patch

# or, without committing
git apply /path/to/devices/27c6:55b4/patches/0*.patch
```

Then build and install per `../README.md`.
