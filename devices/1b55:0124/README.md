# ZKTeco ZK9500 (USB 1b55:0124)

**Status: Working via a native libfprint driver (LGPL-2.1, no vendor blob).**

External optical USB fingerprint scanner sold by ZKTeco (`ZKTeco Inc. ZK9500`, SilkID family, MCU firmware > 1.4). Captures 300x375 8-bit grayscale frames at 500 DPI over USB Bulk IN `0x82`.

## What was broken

Upstream libfprint has no driver for ZKTeco's `1b55` USB vendor ID. ZKTeco's old experimental Linux SDK bundle (`libzkfp.so` + `libsilkidcap.so`) only targeted the earlier `1b55:0120` revision (which streamed raw 1600x1200 Bayer frames and needed closed-source perspective unwarping) and does not recognise `1b55:0124` or integrate with `fprintd`.

## What the fix does

On `1b55:0124` (MCU > 1.4), the onboard MCU already performs Bayer demosaicing, trapezoid rectification, and cropping in hardware, streaming headerless 300x375 500 DPI frames (`112,500` bytes).

The `zk9500` image driver (`FpImageDevice`, 5 enroll stages) reads the factory CMOS exposure/gain and 6-channel prism LED PWM calibration from EEPROM (`IN 0xE7`), drives the capture state machine over `EP0` vendor requests (`0xE0`..`0xEA`), drains the frame FIFO during finger-off detection, and hands the 500 DPI frames directly to libfprint's built-in NBIS (`mindtct` + `bozorth3`) matcher. No external libraries or proprietary binaries are needed.

The patch also adds `1b55:0124` to libfprint's udev autosuspend denylist, as kernel USB autosuspend otherwise resets the scanner mid-session.

## Build and install

Source repository: [arqueon/zk9500-libfprint](https://github.com/arqueon/zk9500-libfprint) (LGPL-2.1-or-later).

- **Arch:** AUR package [`libfprint-zk9500-git`](https://aur.archlinux.org/packages/libfprint-zk9500-git):

  ```sh
  yay -S libfprint-zk9500-git
  sudo systemctl restart fprintd
  ```

- **Other distros:** apply [`patches/0001-zk9500-add-ZKTeco-ZK9500-1b55-0124-optical-driver.patch`](patches/) to upstream libfprint git master and build per [docs/BUILD.md](../../docs/BUILD.md), or run `./scripts/install-generic-linux.sh` from a clone of [arqueon/zk9500-libfprint](https://github.com/arqueon/zk9500-libfprint) (pass `--with-cs9711` if you also need the [Chipsailing CS9711](../2541:0236/) SIGFM fork in the same build).

## Tested on

- CachyOS / Arch Linux (`libfprint` 1.94.10 / 1.94.100, `fprintd` 1.94.5): enroll, verify, `sudo`, polkit, and Wayland lock-screen authentication, both standalone and alongside a second reader.
