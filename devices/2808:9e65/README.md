# FocalTech (USB 2808:9e65)

FocalTech press-type fingerprint sensor.

## What was broken

Upstream libfprint has no driver for this FocalTech sensor.

## What the fix does

Adds a libfprint driver (works alongside a `focaltech_moc` driver
implementation) providing enroll and verify for this sensor.

## Build and install

See `CREDITS` for the driver repo. General shape (build libfprint with the
FocalTech driver):

```sh
git clone https://github.com/armoredvortex/focaltech_2808-9e65
cd focaltech_2808-9e65
# follow the repo's build steps (meson/ninja into a libfprint tree)
sudo ldconfig
sudo pkill -9 -x fprintd
fprintd-list "$USER"
sudo fprintd-enroll "$USER"
```

## PAM setup

Enable fprintd in your PAM stack (distro helper or `auth sufficient
pam_fprintd.so`). Password fallback stays available.

## Tested on

- Not documented upstream beyond the device ID. Add your distro/hardware if you
  confirm it working.

## License note

The source repo is MIT-licensed (compatible with this hub's LGPL-2.1 scope).
