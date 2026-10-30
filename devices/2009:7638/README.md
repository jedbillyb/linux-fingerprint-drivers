# iStorage ADST / BYD BF5325 (USB 2009:7638)

**Status: Working via a native libfprint driver (LGPL-2.1, no vendor blob).**

External capacitive USB fingerprint dongle reporting `iStorage ADST Fingerprint` (`2009:7638`), built around a **BYD `BF5325`** 160x160 @ 508 DPI sensor (`FW V1.9`) and an **AisinoChip `ACH512`** biometric MCU (`match-on-chip`, 3 enroll touches, 200 on-chip flash slots).

## What was broken

1. Upstream libfprint has no driver for `2009:7638`.
2. The dongle enumerates as a USB Mass Storage SCSI Bulk-Only Transport (`bInterfaceClass = 0x08`) virtual CD-ROM (`/dev/sr0`) originally meant to auto-launch a Windows driver installer. On Linux, `usb-storage`, `cdrom_id`, and `udisks2` bind to interface `0` and poll `TEST UNIT READY`, triggering USB Mass Storage reset storms if anything else talks to the device.

## What the fix does

- Adds the `adst2009` match-on-chip driver (`FpDevice`), speaking the 24-byte little-endian `SZOEMHost` command set (`0xAA55` / `0x55AA`) tunnelled inside vendor SCSI-BOT `CDB 0xEF 0x11` (write) and `0xEF 0x12` (non-blocking poll, `< 2 ms`, returning `24 x 0xAF` while waiting for finger contact).
- Runs each 3-URB `CBW -> Data -> CSW` triplet atomically so SCSI phase alignment cannot tear on cancellation, drains both pending response packets on `CMD_FP_CANCEL (0x0130)`, and releases interface `0` with `G_USB_DEVICE_CLAIM_INTERFACE_NONE` so the kernel does not re-attach `usb-storage` on close.
- Ships an accompanying udev rule (`70-adst-2009-libfprint.rules`) that disables USB autosuspend, tells `udisks2` to ignore the fake `/dev/sr0` block node, and unbinds `usb-storage` on plug-in.

## Build and install

Source repository: [arqueon/adst-2009-libfprint](https://github.com/arqueon/adst-2009-libfprint) (LGPL-2.1-or-later).

- **Arch:** AUR package [`libfprint-adst-2009-git`](https://aur.archlinux.org/packages/libfprint-adst-2009-git) (installs the library, the `usb-storage` unbind udev rule, and helper tools):

  ```sh
  yay -S libfprint-adst-2009-git
  sudo systemctl restart fprintd
  ```

  An OpenCV-free variant against vanilla upstream libfprint is also in `packaging/arch-upstream/PKGBUILD` in the source repo.

- **Other distros:** run `./scripts/install-generic-linux.sh` from a clone of [arqueon/adst-2009-libfprint](https://github.com/arqueon/adst-2009-libfprint) (patches vanilla upstream libfprint, zero OpenCV dependency, and installs the udev rule), or apply [`patches/0001-adst2009-add-ADST-BYD-BF5325-2009-7638-match-on-chip.patch`](patches/) per [docs/BUILD.md](../../docs/BUILD.md) and install `/etc/udev/rules.d/70-adst-2009-libfprint.rules`:

  ```udev
  ACTION=="add|change", SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_device", ATTR{idVendor}=="2009", ATTR{idProduct}=="7638", TAG+="uaccess", ENV{ID_LIBFPRINT_DRIVER}="adst2009", TEST=="power/control", ATTR{power/control}="on"
  ACTION=="add|bind", SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_interface", ATTRS{idVendor}=="2009", ATTRS{idProduct}=="7638", DRIVER=="usb-storage", RUN+="/bin/sh -c 'echo -n $kernel > /sys/bus/usb/drivers/usb-storage/unbind'"
  SUBSYSTEM=="block", ENV{ID_VENDOR_ID}=="2009", ENV{ID_MODEL_ID}=="7638", ENV{UDISKS_IGNORE}="1", OPTIONS+="nowatch"
  ```

  Reload udev (`sudo udevadm control --reload && sudo udevadm trigger --attr-match=idVendor=2009`) or replug the reader after installing the rule.

## Tested on

- CachyOS / Arch Linux (`BF5325 FW V1.9` / `ACH512`, `libfprint` 1.94.10 / 1.94.100, `fprintd` 1.94.5): 3-touch enroll, verify, cancel/reopen cycling, `sudo`, polkit, and lock screen.
