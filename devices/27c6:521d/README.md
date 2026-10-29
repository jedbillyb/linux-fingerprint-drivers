# Goodix 521d (USB 27c6:521d, 27c6:538d)

**Status: WIP (27c6:521d via the `libfprint-goodix-521d` AUR package; 27c6:538d verified working via a community SIGFM fork plus a one-time sensor init, see below)**

Goodix fingerprint sensor. The packaged driver also covers `27c6:538d`.

## What was broken

Upstream libfprint has no driver for this Goodix sensor, so it is unrecognised.

## What the fix does

A community Goodix driver (from the goodix-fp-linux-dev project) adds support for
this sensor. For `27c6:521d` it is most easily consumed as the Arch AUR package
`libfprint-goodix-521d`, which builds a patched libfprint (currently based on
1.94.1) with the driver included.

## Build and install

Arch / AUR (easiest, `27c6:521d`):

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

## `27c6:538d` notes (verified on a Dell Inspiron 5405, 2026-10-29)

On `27c6:538d` the sensor speaks Goodix's TLS protocol and the AUR 1.94.1 fork is
not enough on its own: two extra things are needed.

1. **A newer community fork.** Use
   [lbssousa/libfprint](https://github.com/lbssousa/libfprint), branch
   `goodix-538d-sigfm-gtls` (v1.94.100-goodix538d.1). It adds the
   `goodixtls53xd` driver on top of libfprint 1.94.100 with a SIGFM matcher,
   16 enroll stages and cross-session FPN calibration. Install it side by side
   (own directory plus an `/etc/ld.so.conf.d/00-...conf` entry that sorts before
   the distro one) and restart `fprintd`; the distro `libfprint` package can stay
   installed as the fallback. `ldd /usr/lib/fprintd` must resolve to the new
   library, and `fprintd-list "$USER"` should then show
   "Goodix TLS Fingerprint Sensor 53XD".

2. **A one-time MCU initialisation.** A sensor that was paired with Windows
   reports a PSK the community driver cannot know, and the driver then fails
   with `MCU has no config` / `Invalid device PSK`. `goodix-fp-dump`'s
   `run_538d.py` repairs this, but it must run with `fprintd` stopped and the
   device USB-reset first (upstream issue #13: otherwise its first command fails
   with `Invalid message protocol`). If it stops right after `0xa4` with
   `Failed to read PSK` (the erased application keeps running until the MCU is
   reset), the remaining steps are: soft MCU reset (`0xa2`, bit 1) until the
   device re-enumerates and reports `MILAN_GM168SEC_IAP_10007`; then write the
   white-box PSK (`0xe0`, flags `0xbb010003`); flash
   `GF5298_GM168SEC_APP_13016` (`0xf0`, 95 x 256-byte blocks, then the `0xf4`
   HMAC check) and reset. Expected final state: firmware
   `GF5298_GM168SEC_APP_13016` and `preset_psk_read` returning
   `sha256(32 zero bytes)` = `66687aad...`, i.e. the public community PSK. This
   re-flash makes Windows Hello re-pair on the next Windows boot.

Then enroll the same finger twice (16 presses per session, varying the angle):
the second session adds a second template plus the cross-session calibration
the matcher uses. An occasional badly placed press scores 0; that is placement,
not a reason to lower the matcher threshold.

## PAM setup

Enable fprintd in your PAM stack: distro helper where there is one, otherwise
`auth sufficient pam_fprintd.so`. Never `required`. Full steps per distro are in
[docs/BUILD.md](../../docs/BUILD.md#6-pam-setup-login--sudo--lock-screen).

## Tested on

- Arch Linux via the `libfprint-goodix-521d` AUR package.
- Dell Inspiron 5405 (`27c6:538d`, firmware `GF5298_GM168SEC_APP_13016`),
  CachyOS/Arch, kernel 7.1.2, fprintd 1.94.5, 2026-10-29: driver from
  [lbssousa/libfprint](https://github.com/lbssousa/libfprint) branch
  `goodix-538d-sigfm-gtls` (commit `a1bde74`) installed side by side; one-time
  `goodix-fp-dump` init as above; 16-stage enrollment completed and
  `fprintd-verify` reported `verify-match` (SIGFM score 332 vs threshold 24); a
  non-enrolled finger was rejected (score 0).
