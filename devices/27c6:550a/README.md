# Goodix 550a - vendor TOD blob route (USB 27c6:550a)

**Status: Works, but only via a proprietary vendor driver. Nothing open exists.**

> **This entry hosts no code.** It documents the only route that currently works
> for this sensor: Goodix's closed-source driver, shipped by Lenovo as a libfprint
> **TOD** (Touch OEM Driver) module. The blob is not LGPL-2.1 and is not
> redistributed here. Cataloguing it is not an endorsement - see
> [caveats](#caveats).

Very common: Lenovo ThinkPad E14/E15 and ThinkBook models of that generation.

## What was broken

Upstream libfprint has no driver for `27c6:550a`, and no reverse-engineering
effort has produced a working open driver. The goodixtls work covers other
Goodix families (see [`27c6:55b4`](../27c6:55b4/), [`27c6:5110`](../27c6:5110/))
but not this one.

## The TOD route

libfprint supports out-of-tree binary drivers through TOD. Lenovo publishes the
Goodix TOD module for Ubuntu, and community packaging wraps it for other distros.

| Distro | Route |
|--------|-------|
| Ubuntu / Debian | Lenovo's driver package, `libfprint-2-tod1-goodix` (Lenovo E14 Gen 4 Ubuntu driver bundle, [r1slg01w.zip](https://download.lenovo.com/pccbbs/mobiles/r1slg01w.zip)) |
| Arch | AUR `libfprint-2-tod1-goodix` (packages the same Lenovo bundle) |
| Fedora | community RPM packaging of the same blob, e.g. [antidoid/libfprint-tod-goodix-0.0.9](https://github.com/antidoid/libfprint-tod-goodix-0.0.9) (MIT packaging around the proprietary driver) |

You also need a TOD-enabled libfprint (`libfprint-tod` on Arch,
`libfprint-2-2` + TOD on Ubuntu), because stock libfprint does not load TOD
modules.

After install, restart fprintd and enroll as usual; PAM setup is standard, see
[docs/BUILD.md](../../docs/BUILD.md#6-pam-setup-login--sudo--lock-screen).

## Caveats

- Closed-source binary handling your biometric data, with no audit possible.
- x86-64 only, and tied to specific libfprint TOD ABI versions: a libfprint
  update can break it until the packaging catches up.
- Lenovo publishes it for their own hardware; it is not a general-purpose driver.
- If you would rather have no vendor blob in your auth stack, there is currently
  no alternative for this sensor. A reverse-engineering effort would be very
  welcome.

## Tested on

- Widely reported working on Ubuntu (Lenovo's own packaging) and Arch (AUR).
- Fedora via community RPM packaging.
- Reports with model + distro + libfprint version are welcome.

## License note

The Goodix TOD driver is proprietary. This hub hosts only LGPL-2.1 code, so
nothing from it is mirrored here; the packaging repos linked above carry their own
licenses (the packaging, not the blob).
