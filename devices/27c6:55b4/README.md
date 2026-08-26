# Goodix GF3268 (USB 27c6:55b4)

**Status: Working (enroll + verify reliable) via a patched fork.**

Goodix TLS fingerprint sensor, reported by libfprint as **Goodix TLS Fingerprint
Sensor 55X4**. Confirmed firmware revisions include
`GF3268_RTSEC_APP_10042` and `GF3268_RTSEC_APP_10056`. Found in various laptops
behind the Goodix `27c6` vendor ID.

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

## Build and install

Follow [docs/BUILD.md](../../docs/BUILD.md) for dependencies, install, PAM setup,
package pinning and troubleshooting. The only sensor-specific part is which
source to build:

```sh
git clone https://github.com/jedbillyb/libfprint.git   # see CREDITS
cd libfprint
git checkout goodix-55b4-fixes
```

Alternatively, apply the patch series in [`patches/`](patches/) on top of the
upstream base commit named in [`patches/README.md`](patches/README.md).

After installing, `fprintd-list "$USER"` should name **Goodix TLS Fingerprint
Sensor 55X4**.

### Arch / Omarchy notes

Arch currently exposes OpenCV 5 through `opencv5.pc`. If Meson fails with
`Dependency "opencv4" not found`, change the sigfm dependency in
`libfprint/sigfm/meson.build` for that build:

```meson
opencv = dependency('opencv5', required: true)
```

When packaging the patched library locally, the package must satisfy both the
package and shared-library dependencies used by Arch's `fprintd` package:

```bash
provides=('libfprint=1.94.6' 'libfprint-2.so=2-64')
conflicts=('libfprint' 'libfprint-git')
```

Omarchy's stock fingerprint wizard explicitly installs the repository
`libfprint` package. Pacman will then offer to remove the custom Goodix package,
which returns this sensor to an unsupported driver. Install `fprintd` directly,
then enroll and verify with the commands below instead of rerunning the stock
wizard.

For Omarchy lock-screen integration, create its dedicated PAM service only
after enrollment and verification succeed:

```bash
printf '%s\n' \
  '#%PAM-1.0' \
  'auth       required                    pam_fprintd.so' \
  'account    include                     system-local-login' |
  sudo tee /etc/pam.d/omarchy-lock-fingerprint >/dev/null
```

This service is used only for the fingerprint path; Omarchy keeps password
unlock as a separate fallback.

## Enroll

```sh
fprintd-enroll "$USER"    # press repeatedly, vary angle/edge/pressure
fprintd-verify "$USER"    # want: verify-match
```

This sensor is small and the matcher is sigfm-based, so enrollment quality
matters more than usual: if verify fails at odd angles, delete the print
(`fprintd-delete "$USER"`) and re-enroll with deliberately varied finger
positions.

## Tested on

- **Lenovo IdeaPad Flex 5 16ABR8** (82XY) on **Void Linux** (libfprint 1.94.6,
  fprintd) - login, sudo, and screen-lock unlock all working.
- **Lenovo IdeaPad Flex 5 14ARE05** (81X2) on **Omarchy / Arch Linux**
  (firmware `GF3268_RTSEC_APP_10042`, libfprint 1.94.6, fprintd 1.94.5) -
  enrollment, verification, and Omarchy screen-lock unlock all working.
