# Goodix GXFP5187 (SPI)

**Status: working**

Enrols and verifies through `fprintd` and GNOME Settings; session unlock and
`sudo` work. Not a USB sensor: it sits on SPI, ACPI id `GXFP5187`.

Upstream libfprint has no driver for this sensor (tracked in
[libfprint issue #112](https://gitlab.freedesktop.org/libfprint/libfprint/-/issues/112)).
This entry points at an out-of-tree **TOD** driver (a shared module libfprint
loads at runtime), not a patch against libfprint's own sources. See
[patches/](patches/) for the base version and where the code lives.

The driver, its full protocol write-up and the reasoning behind the matcher are
in the source repository:

**https://github.com/Sigfrodr/libfprint-goodixtls**

## What is different about this sensor

Only the deltas from the shared [../../docs/BUILD.md](../../docs/BUILD.md) steps
are listed here.

- **It is SPI, not USB.** libfprint reaches it through the `spidev` node. The
  `spidev` kernel module must be bound to the SPI device (`spi-GXFP5187:00`);
  the driver ships a udev rule that does this on every appearance. `spidev` has
  no alias for this hardware, so nothing loads it on its own, so the install
  step forces it.
- **`spidev` must be given a larger buffer.** The image arrives as a single
  ~22 kB SPI transfer, above the 4096-byte default; `options spidev
  bufsiz=65536` is mandatory or the transfer is truncated and capture fails.
- **A hardware GPIO reset line** (GPIO 58 on `gpiochip0`, per the ACPI `_CRS`)
  is pulsed by the driver to recover the sensor. `gx-recover.sh` in the source
  repo unbinds/rebinds `spidev` and pulses it when the sensor deep-locks.
- **No NBIS.** The sensor is ~6×5 mm and yields far too few minutiae for
  bozorth3, so the driver carries its own SIFT-like matcher. Nothing to install
  for it; it is built into the module.
- **TLS-PSK without Intel ME / SGX.** The pre-shared key is read from the
  sensor's own RAM; stock OpenSSL is used, no patched crypto library.

Build and install (dependencies, `meson`/`ninja`, the spidev bind, the udev
rule and the systemd drop-in) are automated by `sudo ./install.sh` in the
source repository. Session unlock is the generic PAM step from
[../../docs/BUILD.md](../../docs/BUILD.md).

## Tested on

- **Ubuntu 24.04.4 LTS**, GNOME Shell 46, `libfprint-2-tod1` 1.94.7+tod1.
- Hardware: **Huawei MateBook X Pro** (`MACH-WX9`), sensor firmware
  `GF3288_ST411SEC_APP_11033`.
