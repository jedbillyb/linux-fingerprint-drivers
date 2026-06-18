# Goodix newer sensors - experimental driver (USB 27c6:5110 and family)

**Status: WIP / EXPERIMENTAL - not ready for daily use.**

> This is early-stage, actively-developed code from the goodix-fp-linux-dev
> project. It is explicitly **experimental**: expect breakage, unreliable
> enroll/verify, and possible device re-provisioning. Do not rely on it as your
> only authentication method - always keep password login working.

This entry tracks the broader goodix-fp-linux-dev experimental libfprint fork,
which aims to support newer Goodix sensors that have no upstream driver.

## Target devices

- `27c6:5110` (80x64 resolution) is the sensor currently being worked on
  ("Currently in the works: 27c6x5110").
- The project is the umbrella effort behind several Goodix drivers; other newer
  `27c6:*` IDs may be added over time. Check the repo for the current list.

## What was broken

Upstream libfprint has no driver for these newer Goodix sensors; they require
reverse engineering (encrypted protocol, per-device PSK provisioning).

## How to try it

The code lives in the experimental fork (see `CREDITS`). Build it like any
libfprint from source (see the [`27c6:55b4`](../27c6:55b4/) entry for the general
meson/ninja + PAM steps), but treat it as throwaway/testing:

```sh
git clone https://github.com/goodix-fp-linux-dev/libfprint
cd libfprint
# follow the project's current build/run instructions; the driver is unstable
```

The related `goodix-fp-dump` repo holds firmware/protocol tooling used during
development.

## Tested on

- Development/testing only. No stable, daily-use configuration is claimed.
