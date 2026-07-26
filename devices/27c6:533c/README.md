# Goodix 533c - Dell OEM TOD blob route (USB 27c6:533c)

**Status: Works, but only via Dell's proprietary OEM driver.**

> **This entry hosts no code.** It documents the vendor route: Goodix's
> closed-source driver as packaged by Dell for their Ubuntu OEM images. Not
> LGPL-2.1, not redistributed here.

Found on **Dell XPS 13 9300** and **Dell XPS 15 9500**.

## What was broken

Upstream libfprint has no driver for `27c6:533c`, and there is no open
alternative.

## The TOD route

Dell maintains the driver in their OEM Launchpad repository, which is the
authoritative source:

- <https://git.launchpad.net/~oem-solutions-engineers/libfprint-2-tod1-goodix/+git/libfprint-2-tod1-goodix/>

| Distro | Route |
|--------|-------|
| Ubuntu | Dell's OEM archive package `libfprint-2-tod1-goodix` |
| Arch | AUR `libfprint-2-tod1-xps9300-bin` (repackages Dell's Ubuntu binary directly) |
| Other | Extract Dell's `.deb` and install the TOD module manually against a TOD-enabled libfprint |

A TOD-enabled libfprint is required (`libfprint-tod` on Arch).

## Caveats

Same as any TOD blob: closed source, x86-64 only, tied to a libfprint TOD ABI, and
maintained for Dell's own hardware. Keep password auth working.

## Tested on

- Dell XPS 13 9300 on Ubuntu (Dell's own packaging) and Arch (AUR package, 13
  votes and long-standing).
- Reports for XPS 15 9500 welcome.

## License note

Proprietary vendor driver; nothing mirrored here. The Arch packaging is a
build recipe that downloads Dell's binary at install time.
