# Chipsailing CS9711 (USB 2541:0236, 2541:9711)

**Status: Working via a maintained community fork (LGPL-2.1, no vendor blob).**

Chipsailing "CS9711Fingprint" press sensor, 34x236 px. Sold as the built-in
reader on several handhelds and mini PCs: **GPD Win Max 2**, **AYANEO 2**, GTR5
mini, and similar.

## What was broken

Upstream libfprint has no `cs9711` driver, so both product IDs are unrecognised
and were on the libfprint wiki's unsupported list.

## What the fix does

Adds a `cs9711` image driver (press type, 15 enroll stages) that uses the
**sigfm** matcher rather than NBIS, because the 34x236 captures are too small for
minutiae extraction. Fully open, LGPL-2.1, no vendor blob.

## Build and install

Maintained fork: [archeYR/libfprint-CS9711](https://github.com/archeYR/libfprint-CS9711)
(LGPL-2.1). The original ddlsmurf repo is explicitly unmaintained and points here.

Arch (easiest): AUR package `libfprint-cs9711-rebase-git`.

```sh
yay -S libfprint-cs9711-rebase-git
```

Other distros: build the fork from source per [docs/BUILD.md](../../docs/BUILD.md).
The driver needs OpenCV for sigfm, so configure with sigfm enabled.

## Tested on

- Arch Linux via the AUR packages (`libfprint-cs9711-git`,
  `libfprint-cs9711-rebase-git`), on GPD Win Max 2 and AYANEO 2 class hardware.
- Report your handheld and distro so this can be confirmed more widely.
