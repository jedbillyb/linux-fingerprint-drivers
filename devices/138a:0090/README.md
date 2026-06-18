# Validity / Synaptics VFS0090 (USB 138a:0090, 138a:0097)

Validity Sensors (now Synaptics) fingerprint reader, found in 2016-era ThinkPad
laptops. This entry covers `138a:0090` and `138a:0097`.

## What was broken

Upstream libfprint has no native driver for these Validity readers; the protocol
had to be reverse engineered. They are unrecognised by stock libfprint.

## What the fix does

Adds a `vfs0090` driver that does **match-on-host**: it captures images from the
sensor and matches them using libfprint's image comparison algorithm. Most of
the device interaction and crypto comes from the Validity90 reverse-engineering
prototype.

Note: for `138a:0097`, match-on-chip is the only supported path on some
firmware; behaviour can vary by unit.

There is also an unmerged upstream effort for this sensor family: libfprint MR
[!579](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/579)
("validity: Add new driver for Validity/Synaptics VCSFW sensors", Draft; covers
138a:0090/0097/009d and 06cb:009a).

## Build and install

The driver lives on the **`vfs0090`** branch of 3v1n0's libfprint fork (see
`CREDITS`). Packaged builds exist:

- Ubuntu: PPA `ppa:3v1n0/libfprint-vfs0090`
- Arch: AUR package
- NixOS: in nixpkgs

From source:

```sh
git clone https://github.com/3v1n0/libfprint
cd libfprint
git checkout vfs0090
meson setup builddir --prefix=/usr
meson compile -C builddir
sudo meson install -C "$PWD/builddir"
sudo ldconfig
```

Then restart fprintd and enroll:

```sh
sudo pkill -9 -x fprintd
fprintd-list "$USER"
sudo fprintd-enroll "$USER"
```

## PAM setup

Enable fprintd in your PAM stack (distro helper or `auth sufficient
pam_fprintd.so`). Password fallback stays available.

## Tested on

- Ubuntu (PPA), Arch Linux (AUR), Fedora 28, NixOS.
