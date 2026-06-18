# FPC Match-on-Host / fpcmoh (USB 10a5:9800)

Fingerprint Cards (FPC) sensor.

## Hardware

Seen on ThinkPad E14 Gen5.

## What was broken

Upstream libfprint does not support this FPC sensor, so it is unrecognised.

## What the fix does

Adds the `fpcmoh` (FPC match-on-host) driver to libfprint plus the udev rules
needed for the device, enabling enroll and verify.

## Build and install

The cleanest source is xuwd1's AUR package `libfprint-fpcmoh-git` (see
`CREDITS`). Arch:

```sh
# AUR helper, e.g.
yay -S libfprint-fpcmoh-git
sudo pkill -9 -x fprintd
fprintd-list "$USER"
sudo fprintd-enroll "$USER"
```

On other distros, build libfprint with the fpcmoh driver from that source and
install the accompanying udev rules. furcom's repo (archived, read-only) packaged
this for Fedora/dnf.

## PAM setup

Enable fprintd in your PAM stack (distro helper or `auth sufficient
pam_fprintd.so`). Password fallback stays available.

## Tested on

- ThinkPad E14 Gen5: Fedora (furcom's packaging); Arch via the AUR package.
