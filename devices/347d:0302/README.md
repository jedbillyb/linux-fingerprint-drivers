# Blestech Betterlife btlfp (USB 347d:0302, 347d:0304)

**Status: Working via native libfprint drivers (LGPL-2.1, no vendor blob).**

Capacitive USB fingerprint sensors from Blestech / Shenzhen Betterlife (`btlfp Betterlife Fingerprint`) sharing an SM2/SM3/SM4 encrypted Bulk USB framing (`EP 0x02 OUT`, `EP 0x81 IN`):

- **`347d:0302`** (scheme `0x10`, chip `0x5f83`, 112x96): **match-on-chip** (`betterlife347d_moc`, `FpDevice`), 10 on-chip flash template slots, 7 enroll stages (8 touches total including libfprint's initial duplicate check).
- **`347d:0304`** (scheme `0x11`, 96x112): **match-on-host** (`betterlife347d`, `FpImageDevice`), streams decrypted 96x112 captures to the host.

## What was broken

Upstream libfprint has no driver for the `347d` vendor ID, so neither sensor is recognised.

## What the fix does

Both sensors establish an ephemeral session key on open (`0xA2`) using **SM2** ECDH (`OpenSSL 3`), **SM3** KDF/MAC verification, and per-frame **SM4-ECB** nonce-derived keys:

- `betterlife347d_moc` (`347d:0302`) drives on-chip enrollment (`0xB0`), 1:N identification (`0xB1`), template deletion/storage clear (`0xB2`), and slot queries (`0xB3`), exposing the silicon UID (`0xC0`) to `fprintd`. Firmware-update and bootloader opcodes (`0xD0`..`0xD2`, `0xC3`) are omitted.
- `betterlife347d` (`347d:0304`) streams 96x112 grayscale frames. It compiles against vanilla upstream libfprint (falling back to NBIS), but because 96x112 captures yield very few minutiae, **`347d:0304` users should build on top of a SIGFM-enabled libfprint tree** (such as [archeYR/libfprint-CS9711](https://github.com/archeYR/libfprint-CS9711), which the default AUR package and installer script use). `347d:0302` matches on the sensor MCU and works identically on vanilla upstream libfprint without OpenCV.

## Build and install

Source repository: [arqueon/betterlife-347d-libfprint](https://github.com/arqueon/betterlife-347d-libfprint) (LGPL-2.1-or-later).

- **Arch:** AUR package [`libfprint-betterlife-347d-git`](https://aur.archlinux.org/packages/libfprint-betterlife-347d-git) (built on `libfprint-CS9711` with SIGFM for both `347d:0302` and `347d:0304`, OpenCV 4 and 5 compatible):

  ```sh
  yay -S libfprint-betterlife-347d-git
  sudo systemctl restart fprintd
  ```

  If you only have `347d:0302` and want to avoid pulling in OpenCV, build `packaging/arch-upstream/PKGBUILD` from the source repo against vanilla upstream libfprint.

- **Other distros:**
  - For **`347d:0302` (MOC)** without OpenCV: apply [`patches/0001-betterlife347d-add-Blestech-Betterlife-347d-0302-and.patch`](patches/) to upstream libfprint git master (requires `openssl` >= 3.0 dev headers) and build per [docs/BUILD.md](../../docs/BUILD.md), or run `./scripts/install-generic-linux.sh --upstream-only` from the source repo.
  - For **`347d:0304` (MOH)** (or both): install OpenCV dev headers and run `./scripts/install-generic-linux.sh` from [arqueon/betterlife-347d-libfprint](https://github.com/arqueon/betterlife-347d-libfprint) so `betterlife347d` links against SIGFM.

## Tested on

- **`347d:0302` (MOC):** CachyOS / Arch Linux (chip `0x5f83`, firmware `proj=0x0f00 V1.0.0.0`, `libfprint` 1.94.10 / 1.94.100, `fprintd` 1.94.5): enroll (7/7 stages), verify, `sudo`, polkit, and lock screen.
- **`347d:0304` (MOH):** Linux (`fprintd` + SIGFM build; capture and SM2/SM3/SM4 framing originally validated in [Light-log/betterlife-347d-0304-fingerprint-linux](https://github.com/Light-log/betterlife-347d-0304-fingerprint-linux)).
