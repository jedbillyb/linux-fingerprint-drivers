# FPC Sensor Controller L:0001 - fingerprint-ocv (USB 10a5:9201)

**Status: Works via a standalone AGPL-3.0 project, not a libfprint driver.**

> **This entry hosts no code.** The working driver is
> [vrolife/fingerprint-ocv](https://github.com/vrolife/fingerprint-ocv), which is
> **AGPL-3.0** and therefore cannot be mirrored into this LGPL-2.1 hub. It is
> catalogued here because it works and people with this sensor should be able to
> find it.

FPC sensor controller reporting `L:0001 FW:021.26.2.x`. Found on RedmiBook 14 Pro
2022 and similar Xiaomi/Redmi models.

## What was broken

Upstream libfprint has no driver. The in-tree FPC work covers other controllers:
see [`10a5:9800`](../10a5:9800/) (fpcmoh) and [`10a5:9200`](../10a5:9200/)
(FPC1022, WIP).

## The fingerprint-ocv route

fingerprint-ocv (40+ stars, AGPL-3.0) is a standalone daemon rather than a
libfprint driver: it drives the sensor and does matching with OpenCV, then exposes
authentication to the system itself. Follow that project's own build and setup
instructions.

Because it is not a libfprint driver, the generic steps in
[docs/BUILD.md](../../docs/BUILD.md) mostly do not apply; its PAM integration is
its own.

Note the project's last release activity was 2022, so expect to fix build issues
against current toolchains.

## Caveats

- AGPL-3.0: fine to use, incompatible with contributing it into libfprint or this
  hub. If you want this sensor supported upstream, it needs a clean-room
  LGPL-2.1 driver.
- Not a libfprint driver, so fprintd-based tooling and desktop integrations may
  behave differently.

## Tested on

- Reported working by that project's users on RedmiBook-class hardware.
- Distro reports welcome.

## License note

AGPL-3.0. Catalogued as a pointer only; no code from it is present in this repo.
