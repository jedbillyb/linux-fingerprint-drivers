# Goodix GF3268 (USB 27c6:55b4)

**Status: Working via TheWeirdDev's goodix55b4 driver (native Milan matcher). The older goodixtls55x4 fork below is deprecated.**

Goodix TLS fingerprint sensor (GF3268). Confirmed firmware revisions include
`GF3268_RTSEC_APP_10041`, `GF3268_RTSEC_APP_10042` and
`GF3268_RTSEC_APP_10056`. Found in various laptops behind the Goodix `27c6`
vendor ID. The same driver also supports `27c6:5584`, which is the same die
with a different USB PID.

## What was broken

Upstream libfprint has no driver for this sensor; it lists `55b4` as
unsupported. The closest upstream work is the goodixtls driver for the `511`
family, which does not recognise the `55b4` product ID or its firmware family.

## The driver

[TheWeirdDev/libfprint-goodix55b4-milan](https://github.com/TheWeirdDev/libfprint-goodix55b4-milan)
is a `goodix55b4` driver on top of upstream libfprint 1.94.100, with every
normal libfprint driver kept. It:

- talks to the sensor over TLS with the all-zero pre-shared key (PSK), and
  refuses to start if the sensor holds a different one,
- accepts any `GF3268_RTSEC_APP_*` firmware,
- matches with Goodix's Milan matcher, ported to native C (no Windows DLL).

Its author reports a 95% first-try identify rate, against 71% for the SIGFM
matcher the old driver used, with no false accepts on their test set.

## Install

Follow the driver's own
[README](https://github.com/TheWeirdDev/libfprint-goodix55b4-milan#readme).
It has:

- **Arch:** AUR package `libfprint-goodix55b4`.
- **Debian 12/13, Ubuntu 24.04/26.04, Fedora 43/44:** prebuilt packages on
  each [release](https://github.com/TheWeirdDev/libfprint-goodix55b4-milan/releases/latest).
- **Other distros:** build it from source, see its README.

Each package replaces the distro's `libfprint`; fprintd keeps working.

### Sensor provisioning

The driver needs the sensor to hold the all-zero PSK. If `fprintd-enroll`
fails with `Sensor is not provisioned with the zero PSK`, follow the
driver's
[Sensor provisioning](https://github.com/TheWeirdDev/libfprint-goodix55b4-milan#sensor-provisioning-one-time)
section. This overwrites the PSK Windows paired, so Windows Hello stops
working with the sensor, and on firmware other than `10041` it involves a
firmware flash. Read the warnings there first.

**Sensors already set up with the old fork below do not need this.** The old
fork wrote the same zero PSK (it checks the same PSK hash with the same
flags), so the new driver accepts the sensor as it is.

## Moving from the old fork

Prints from the old driver are not compatible with the new one.

1. Remove the old patched library. If you pinned or held your distro's
   `libfprint` package for it, unhold it.
2. Install the new driver as above, then restart fprintd.
3. Delete the old prints (`sudo rm -rf /var/lib/fprint/<user>/goodixtls55x4`)
   and enroll again: `fprintd-enroll "$USER"`, then `fprintd-verify "$USER"`.

Your PAM setup (`pam_fprintd.so`) does not change.

### Arch / Omarchy notes

Omarchy's stock fingerprint wizard explicitly installs the repository
`libfprint` package, and pacman will offer to remove the Goodix package to do
it, which leaves the sensor without a driver. Install `fprintd` directly and
enroll with the commands above instead of rerunning the wizard.

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

## Tested on

- New driver: tested by its author; see the driver's README for hardware
  and results. Packages are built for Arch, Debian, Ubuntu and Fedora.
- Old fork: **Lenovo IdeaPad Flex 5 16ABR8** (82XY) on **Void Linux**
  (firmware `GF3268_RTSEC_APP_10056`, libfprint 1.94.6): login, sudo and
  screen-lock unlock.
- Old fork: **Lenovo IdeaPad Flex 5 14ARE05** (81X2) on **Omarchy / Arch
  Linux** (firmware `GF3268_RTSEC_APP_10042`, libfprint 1.94.6, fprintd
  1.94.5): enrollment, verification and Omarchy screen-lock unlock.

## Deprecated: the goodixtls55x4 fork

Before the driver above existed, this entry pointed at a patched fork of
TheWeirdDev's older goodixtls libfprint work:
[jedbillyb/libfprint](https://github.com/jedbillyb/libfprint), branch
`goodix-55b4-fixes`, with the same changes exported in [`patches/`](patches/).
TheWeirdDev has deprecated that base: it was less accurate, had known bugs,
and is no longer supported. It still works on machines that already run it,
but new installs should use the driver above, and existing ones should move
when convenient.

What the fork changed, for reference: it accepts the `GF3268_RTSEC_APP_10056`
firmware prefix, (re)provisions the zero PSK via a white-box PSK write,
corrects the `goodix_send_preset_psk_write` framing, enables the PSK ciphers
at `SECLEVEL=0` in the TLS server, and tunes the SIGFM thresholds.

To build it anyway, follow [docs/BUILD.md](../../docs/BUILD.md) with:

```sh
git clone https://github.com/jedbillyb/libfprint.git
cd libfprint
git checkout goodix-55b4-fixes
```

On Arch, OpenCV 5 is exposed as `opencv5.pc`; if Meson fails with
`Dependency "opencv4" not found`, change the SIGFM dependency in
`libfprint/sigfm/meson.build` to `dependency('opencv5', required: true)`.
