# Goodix 521d (USB 27c6:521d, 27c6:538d)

**Status: WIP (works via the `libfprint-goodix-521d` AUR package)**

Goodix fingerprint sensor. The packaged driver also covers `27c6:538d`.

## What was broken

Upstream libfprint has no driver for this Goodix sensor, so it is unrecognised.

## What the fix does

A community Goodix driver (from the goodix-fp-linux-dev project) adds support for
this sensor. It is most easily consumed as the Arch AUR package
`libfprint-goodix-521d`, which builds a patched libfprint (currently based on
1.94.1) with the driver included.

## Build and install

Arch / AUR (easiest):

```sh
# with an AUR helper
yay -S libfprint-goodix-521d
sudo pkill -9 -x fprintd
fprintd-list "$USER"
sudo fprintd-enroll "$USER"
```

On other distros, build libfprint from the goodix-fp-linux-dev source (see
`CREDITS`) the same way as any libfprint-from-source build (see the
[`27c6:55b4`](../27c6:55b4/) entry for the general meson/ninja + PAM steps).

## PAM setup

Enable fprintd in your PAM stack (distro helper or `auth sufficient
pam_fprintd.so`). Password fallback stays available.

## Tested on

- Arch Linux via the `libfprint-goodix-521d` AUR package.
