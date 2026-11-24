# Synaptics "Prometheus" / "Metallica MIS Touch" (USB 06cb:009a)

**Status: Working - via python-validity (userspace daemon), or via a native libfprint-2-tod1 driver from a community fork (Arch package; needs a one-time firmware upload).**

Synaptics/Validity "Prometheus" fingerprint readers. The python-validity driver
covers `06cb:009a` (Metallica MIS Touch) and the Validity `138a:0090`,
`138a:0097`, `138a:009d` family.

> Overlap note: `138a:0090`/`138a:0097` also have a libfprint match-on-host
> driver entry at [`138a:0090`](../138a:0090/). python-validity is the
> match-on-chip userspace path and is usually the better bet for `06cb:009a` and
> `138a:009d`.

Two routes work for this sensor and **they cannot coexist**: both claim the
reader, and each stack replaces the other's `fprintd`.

| Route | Stack | Availability |
|-------|-------|--------------|
| python-validity | userspace daemon -> open-fprintd -> fprintd / pam_fprintd | Ubuntu PPA, Arch AUR, Fedora COPR |
| native TOD driver | `libfprint-2-tod1` module loaded by a TOD-enabled libfprint -> stock fprintd / pam_fprintd | Arch: AUR `libfprint-2-tod1-synaptics009a` (community fork, not upstream) |

## What was broken

These Synaptics "Prometheus" sensors use match-on-chip and an encrypted (TLS)
protocol that upstream libfprint does not implement. There is an open upstream
effort for this family: MR
[!579](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/579)
("validity: Add new driver for Validity/Synaptics VCSFW sensors") was a draft
that is now closed, continued by the open MR
[!626](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/626)
(0x969/0xd51 sensor support), which also covers `06cb:009a`.

## Route 1: python-validity (userspace daemon)

`python-validity` is **not a libfprint driver**. It is a reverse-engineered
**userspace daemon** that talks to the sensor over DBus. It initialises the
device, then registers itself with the **open-fprintd** service so that the
normal `fprintd` clients and PAM modules work on top of it.

So the stack is: `python-validity` (device driver daemon) -> `open-fprintd`
(fprintd-compatible DBus service) -> `fprintd-clients` / `pam_fprintd`.

### Install

Packages exist for major distros (see `CREDITS`):

- Ubuntu: PPA
- Arch: AUR
- Fedora: COPR

Install `open-fprintd`, `python3-validity`, and `fprintd-clients` together, then:

```sh
sudo systemctl start python3-validity
fprintd-enroll        # plain fprintd clients work via open-fprintd
fprintd-verify
```

Note: on some units the sensor's storage must be initialised/cleared first; see
the project's docs for `validity-sensors-firmware` and `dbus-init` steps.

## Route 2: native libfprint-2-tod1 driver (community fork)

A native Rust driver that implements this sensor's match-on-chip protocol
directly, as a `libfprint-2-tod1` module: matching happens inside the sensor
against templates in its own flash storage. It runs under stock `fprintd`, with
no Python daemon and no `open-fprintd`.

It is a community fork rather than an upstream merge request, and it needs a
**TOD-enabled libfprint**, because stock libfprint does not load TOD modules.

| Distro | Route |
|--------|-------|
| Arch | AUR [`libfprint-2-tod1-synaptics009a`](https://aur.archlinux.org/packages/libfprint-2-tod1-synaptics009a) (packaging: [hustles/libfprint-2-tod1-synaptics009a](https://github.com/hustles/libfprint-2-tod1-synaptics009a)) together with AUR [`libfprint-tod-git`](https://aur.archlinux.org/packages/libfprint-tod-git) |
| Debian / Ubuntu | the driver project publishes a `.deb` of the same driver (see `CREDITS`) |

Remove the python-validity stack first - the two routes cannot share the sensor:

```sh
paru -Rns python-validity open-fprintd fprintd-clients-git
paru -S libfprint-2-tod1-synaptics009a
```

Then the one-time setup. This sensor also needs its **QMatcher firmware
extension** flashed into flash partition 2 before enrollment can succeed at all;
the package does that, generates the host calibration, and restarts `fprintd`:

```sh
sudo synaptics009a-setup
fprintd-enroll -f right-index-finger    # 12 presses; press the oval, do not swipe
fprintd-verify                          # expect: verify-match
```

The firmware extension (`6_07f_lenovo_mis_qm.xpfwext`) ships inside Lenovo's
Windows driver package (`nz3gf07w.exe`); the package downloads it from Lenovo at
build time and does not redistribute it. The capture and initialisation blobs in
the driver originate in Synaptics' Windows driver and are distributed the same
way python-validity distributes them.

### Caveats

- The firmware upload above is required. Without it the sensor fault-resets on
  large capture commands and enrollment never completes, even though init and the
  TLS session appear to work - a confusing failure mode.
- Needs a TOD-enabled libfprint fork, so it is tied to that fork's TOD ABI.
- x86-64 only, and it puts closed sensor firmware in your authentication path.
  The driver itself is source-available under MIT OR LGPL-2.1-or-later.
- Keep password authentication working.

## PAM setup

Both routes end at `fprintd`, so PAM setup is the standard one; see
[docs/BUILD.md](../../docs/BUILD.md#6-pam-setup-login--sudo--lock-screen). The
build sections of that guide do not apply here, since both routes are packaged
rather than built from libfprint source.

## Tested on

- Arch Linux, Lenovo ThinkPad T480: native route (AUR package) - enroll, verify,
  `sudo` and login. python-validity is also reported working on Arch.
- Ubuntu (PPA) and Fedora (COPR) for python-validity.

## License note

- python-validity is MIT-licensed.
- The native driver is MIT OR LGPL-2.1-or-later, as declared in its `Cargo.toml`;
  the upstream repository carries no `LICENSE` file.
- Nothing is mirrored here. The Synaptics capture/init blobs and the Lenovo
  firmware extension are not redistributed by this hub.
