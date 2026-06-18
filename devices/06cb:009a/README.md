# Synaptics "Prometheus" via python-validity (USB 06cb:009a)

Synaptics/Validity "Prometheus" fingerprint readers. The python-validity driver
covers `06cb:009a` (Metallica MIS Touch) and the Validity `138a:0090`,
`138a:0097`, `138a:009d` family.

> Overlap note: `138a:0090`/`138a:0097` also have a libfprint match-on-host
> driver entry at [`138a:0090`](../138a:0090/). python-validity is the
> match-on-chip userspace path and is usually the better bet for `06cb:009a` and
> `138a:009d`.

## What was broken

These Synaptics "Prometheus" sensors use match-on-chip and an encrypted protocol
that upstream libfprint does not implement.

## What the fix does (architecture is different)

`python-validity` is **not a libfprint driver**. It is a reverse-engineered
**userspace daemon** that talks to the sensor over DBus. It initialises the
device, then registers itself with the **open-fprintd** service so that the
normal `fprintd` clients and PAM modules work on top of it.

So the stack is: `python-validity` (device driver daemon) -> `open-fprintd`
(fprintd-compatible DBus service) -> `fprintd-clients` / `pam_fprintd`.

There is also an unmerged upstream effort to support this family natively in
libfprint: MR
[!579](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/579)
("validity: Add new driver for Validity/Synaptics VCSFW sensors", Draft).

## Install

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

## PAM setup

Once open-fprintd is running, configure PAM exactly as for normal fprintd
(distro helper or `auth sufficient pam_fprintd.so`).

## Tested on

- Ubuntu (PPA), Arch Linux (AUR), Fedora (COPR).

## License note

python-validity is MIT-licensed (compatible with this hub's scope). It is listed
here as the canonical working fix even though it is a userspace daemon rather
than a libfprint driver.
