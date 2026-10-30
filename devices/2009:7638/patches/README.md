# Patches for iStorage ADST / BYD BF5325 (2009:7638)

- `0001-adst2009-add-ADST-BYD-BF5325-2009-7638-match-on-chip.patch` - adds the `adst2009` match-on-chip driver (`FpDevice`, 24-byte `SZOEMHost` over vendor SCSI-BOT `0xEF`) and `2009:7638` udev hwdb autosuspend rule against upstream [libfprint](https://gitlab.freedesktop.org/libfprint/libfprint) git master (`version: '1.94.100'`), base commit `6f9479c3d55f847c1b3769f28ceb99227f9858cf` (2026-09-02, "synaptics: Add new PID 0x10b").

Apply with `git am` or `git apply`, build per [docs/BUILD.md](../../../docs/BUILD.md), and install the `usb-storage` unbind udev rule shown in [`../README.md`](../README.md) so the kernel does not claim interface `0` as a virtual CD-ROM (`/dev/sr0`).
