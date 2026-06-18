# Goodix HTK32 (USB 27c6:5385, 27c6:5335, 27c6:5395)

Goodix HTK32 capacitive press-type fingerprint sensor (108 x 88 px). The same
driver covers product IDs `5335`, `5385`, and `5395`.

## Hardware

Seen on Dell XPS 13 9305, Dell XPS 13 7390 2-in-1, and Dell XPS 15 9570.

## What was broken

Upstream libfprint has no driver for these Goodix HTK32 sensors, so they are
unrecognised. The small 108x88 captures are also too small for libfprint's
standard minutiae matching.

## What the fix does

Adds a driver that initialises the sensor via PSK exchange and a GTLS handshake,
detects finger placement through FDT events, captures the encrypted images, and
matches using SIFT-based keypoint analysis (via OpenCV) instead of the standard
minutiae matcher, which the small captures are incompatible with.

## Build and install

Integrates with libfprint v1.94.10. Extra dependencies: **OpenCV 4** and
**OpenSSL 3.0+** on top of the usual libfprint build deps.

```sh
# see CREDITS for the driver repo
git clone https://github.com/AndyHazz/goodix53x5-libfprint
cd goodix53x5-libfprint
./install.sh                       # follow the prompted meson.build edit
meson setup builddir --prefix=/usr
sudo ninja -C builddir install
sudo ldconfig
```

Arch users can install the AUR package `libfprint-goodix53x5` instead.

Then restart fprintd and enroll:

```sh
sudo pkill -9 -x fprintd
fprintd-list "$USER"
sudo fprintd-enroll "$USER"
```

## PAM setup

Enable fprintd in your PAM stack (e.g. add `auth sufficient pam_fprintd.so` to
the relevant `/etc/pam.d` file, or use your distro's helper). Password fallback
stays available.

## Tested on

- Arch Linux, Fedora, and Ubuntu/Debian, on the Dell XPS models listed above.
