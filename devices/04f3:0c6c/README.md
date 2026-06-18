# ELAN Match-on-Chip 2 (USB 04f3:0c6c)

ELAN "Match-on-Chip 2" fingerprint reader.

## What was broken

The device is unsupported by upstream libfprint, so it is unrecognised by stock
installs.

## What the fix does

Adds a driver adapted from Davide Depau's `elanmoc2` driver (originally for
`04f3:0c4c`). The key changes for this sensor, found by analysing the Windows
driver's USB traffic, are 0-indexed hardware slot addressing and an ARM-M4
specific pre-commit slot marker sequence. Enroll and verify are supported.

See also the related ELAN entry: [`04f3:0c4c`](../04f3:0c4c/).

## Build and install

Modifies the core libfprint library. See `CREDITS` for the driver repo; it ships
install instructions for Ubuntu/Debian, Fedora, and Arch. General shape:

```sh
git clone https://github.com/ITx-prash/libfprint-elan-04f3-0c6c
cd libfprint-elan-04f3-0c6c
# follow the repo's per-distro build steps (meson/ninja)
sudo ldconfig
sudo pkill -9 -x fprintd
fprintd-list "$USER"
sudo fprintd-enroll "$USER"
```

> The driver replaces a core system library; use at your own risk and keep a way
> to restore your distro's stock libfprint.

## PAM setup

Enable fprintd in your PAM stack (distro helper or `auth sufficient
pam_fprintd.so`). Password fallback stays available.

## Tested on

- Install steps documented for Ubuntu/Debian, Fedora, and Arch Linux.
