# Goodix GF3268 (USB 27c6:55b4)

Goodix TLS fingerprint sensor, reported by libfprint as **Goodix TLS Fingerprint
Sensor 55X4**. Firmware family `GF3268_RTSEC_APP_10056`. Found in various
laptops behind the Goodix `27c6` vendor ID.

## What was broken

Upstream libfprint has no driver that accepts this device. The closest support
is the goodixtls work for the `511` family, which does not recognise the
`55b4` product ID or its firmware family, and its PSK/TLS handling does not
match this sensor.

## What the fix does

The fix is a patched goodixtls driver (branch linked in `CREDITS`). It:

- Accepts the `GF3268_RTSEC_APP_10056` firmware-family prefix so the device is
  recognised.
- (Re)provisions the device PSK via a white-box PSK write so the host and sensor
  share a key.
- Corrects the `goodix_send_preset_psk_write` wire framing.
- Enables the PSK ciphers at `SECLEVEL=0` in the goodix TLS server so the
  handshake completes.
- Tunes the sigfm matcher thresholds for reliable enroll/verify on this sensor.

## Build and install libfprint from source

These are Void Linux steps; adapt the package manager for your distro. You need
meson, ninja, a C toolchain, and the libfprint build dependencies (glib, nss,
gusb, pixman, etc.).

```sh
# 1. Clone the patched fork (see CREDITS for the URL/branch)
git clone https://github.com/jedbillyb/libfprint.git
cd libfprint
git checkout goodix-55b4-fixes

# 2. Configure and build as your normal user
meson setup builddir
meson compile -C builddir

# 3. Install over the system libfprint (use an absolute path)
sudo meson install -C "$PWD/builddir"
sudo ldconfig

# 4. Restart fprintd and confirm the sensor is detected
sudo pkill -9 -x fprintd
fprintd-list "$USER"   # should list "Goodix TLS Fingerprint Sensor 55X4"
```

Note: installing over the system libfprint may wipe existing enrollments, and if
your distro packages libfprint you may need to hold/pin the package so an update
does not overwrite the patched library.

## Enroll

```sh
sudo fprintd-enroll "$USER"    # press repeatedly, vary angle/edge/pressure
sudo fprintd-verify "$USER"    # want: verify-match
```

If `verify` fails at odd angles, re-enroll with more captures and deliberately
varied finger positions.

## PAM setup

To use the fingerprint for login/sudo/lock screen, add fprintd to your PAM
stack. On Void, add this line to `/etc/pam.d/system-auth` (keep a backup first):

```
auth sufficient pam_fprintd.so
```

`sufficient` means a successful scan authenticates, and your password still works
as a fallback. login, sudo, and screen lockers that chain to `system-auth` pick
this up. On other distros, use the distro's helper (e.g.
`pam-auth-update --enable fprintd` on Debian/Ubuntu) or edit the relevant
`/etc/pam.d` files.

## Tested on

- **Void Linux** (libfprint 1.94.6, fprintd) - login, sudo, and screen-lock
  unlock all working.
