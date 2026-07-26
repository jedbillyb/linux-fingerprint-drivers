# Synaptics Tudor match-in-sensor family (USB 06cb:00ff and relatives)

**Status: Working via two community routes, neither upstream.**

Synaptics "Tudor" match-in-sensor readers. These do enrollment and matching
entirely on the sensor over a TLS-paired channel, which is why libfprint's
in-tree `synaptics` (BMKT) driver cannot drive them.

Device IDs covered (per Synaptics' own `synaWudfBioUsbUwp.inf`):

| USB ID | Notes |
|--------|-------|
| `06cb:00c9` | hardware-tested by the synaTudorMiS author |
| `06cb:00e7` | hardware-tested |
| `06cb:00ff` | hardware-tested |
| `06cb:00d1` | listed in the vendor INF, untested |
| `06cb:0124` | listed in the vendor INF, untested |
| `06cb:0169` | newer driver generation, less explored |

Common on HP EliteBook/ProBook/Envy/Spectre and various Lenovo models.

## What was broken

No upstream libfprint driver. The sensors are claimed by no in-tree driver, or
mis-claimed by `synaptics` without working enroll or verify.

## Route 1: synaTudorMiS (native, open, no vendor blob)

[vojtapl/synaTudorMiS](https://github.com/vojtapl/synaTudorMiS) is a
reverse-engineered native driver (LGPL-2.1, C). The author reports it "just
works" but has paused development short of upstreaming: OpenSSL leaks memory,
some FIXMEs remain, no test suite.

It needs a cleaned libfprint tree plus an fprintd patch for persistent per-device
data (both linked from that repo's README), then builds like any libfprint: see
[docs/BUILD.md](../../docs/BUILD.md).

Choose this route if you want no proprietary code in your auth stack.

## Route 2: synaTudor relinking (uses the vendor Windows driver)

[Popax21/synaTudor](https://github.com/Popax21/synaTudor) (LGPL-2.1, 140+ stars)
takes a different approach: it **relinks Synaptics' own Windows driver binaries
at runtime** on x86-64 Linux and exposes them through a libfprint TOD module. The
project reports itself fully functional.

- Arch: AUR `libfprint-2-tod1-synatudor-git`.
- Other distros: build from the repo; you must supply the vendor Windows driver
  files yourself.

This is the more widely used route, but it runs vendor binary code, is x86-64
only, and its own README warns about bricked sensors and firmware corruption.
Read that warning before starting.

## Pairing caveat (both routes)

The sensor stores host pairing data on-chip. Pairing with Linux can invalidate
your Windows Hello pairing (and vice versa); dual-booters generally cannot share
enrollments. Some flows can clear the sensor's storage.

## PAM setup

Standard fprintd PAM once a route works, see
[docs/BUILD.md](../../docs/BUILD.md#6-pam-setup-login--sudo--lock-screen). Keep
password fallback: both routes are experimental.

## Tested on

- `06cb:00c9`, `06cb:00e7`, `06cb:00ff` confirmed by the synaTudorMiS author.
- synaTudor (route 2) is reported working across many HP and Lenovo models via
  the AUR package.
- Distro/model reports welcome: this entry covers six product IDs and only three
  are directly confirmed.
