# ELAN 0c4b - Lenovo TOD blob route (USB 04f3:0c4b)

**Status: Works, but only via Lenovo's proprietary ELAN driver.**

> **This entry hosts no code.** ELAN's closed-source driver, shipped by Lenovo as
> a libfprint TOD module. Not LGPL-2.1, not redistributed here.

Found on Lenovo ThinkPad E14 Gen 4 and related models.

## What was broken

No upstream libfprint driver for `04f3:0c4b`. The open ELAN match-on-chip work
covers other IDs: see [`04f3:0c4c`](../04f3:0c4c/), [`04f3:0c6c`](../04f3:0c6c/),
[`04f3:0c8e`](../04f3:0c8e/), [`04f3:0c9c`](../04f3:0c9c/).

## The TOD route

Lenovo publishes the ELAN TOD driver in their E14 Gen 4 Ubuntu driver bundle:
[r1sle01w.zip](https://download.lenovo.com/pccbbs/mobiles/r1sle01w.zip).

| Distro | Route |
|--------|-------|
| Ubuntu / Debian | Lenovo's driver bundle (install the `libfprint-2-tod1-elan` deb it contains) |
| Arch | AUR `libfprint-2-tod1-elan` (packages the same bundle) |
| Fedora | community packaging of the same blob exists; verify provenance before use |

Needs a TOD-enabled libfprint.

## Caveats

Closed source, x86-64 only, ABI-tied to libfprint TOD, published for Lenovo
hardware. Keep password auth working.

## Tested on

- Reported working on Lenovo ThinkPad E14 Gen 4, Ubuntu and Arch.
- Reports welcome; this entry is thinner than the open-driver entries.

## License note

Proprietary vendor driver; nothing mirrored here.
