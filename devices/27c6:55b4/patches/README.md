# Patches for Goodix GF3268 (27c6:55b4)

These are `git format-patch` exports of the fix commits from the
`goodix-55b4-fixes` branch (see `../CREDITS`), split one patch per logical fix.

## Apply order

Apply in numeric order:

1. `0001` - accept the `GF3268_RTSEC_APP` firmware family so the device is recognised
2. `0002` - (re)provision the PSK instead of only checking it
3. `0003` - fix the preset PSK write framing
4. `0004` - enable PSK ciphers for the sensor TLS handshake
5. `0005` - tighten the sigfm matching thresholds

## Base

The patches apply on top of the goodixtls libfprint tree at commit
`13ab542` (the last commit before this fix series). If you are starting from the
patched fork directly, you do **not** need these - just build the
`goodix-55b4-fixes` branch as described in `../README.md`. The patches are here
so the fix can be reproduced against a plain libfprint checkout.

## How to apply

```sh
# from inside a libfprint checkout at the base commit
git am /path/to/devices/27c6:55b4/patches/0*.patch

# or, without committing
git apply /path/to/devices/27c6:55b4/patches/0*.patch
```

Then build and install per `../README.md`.
