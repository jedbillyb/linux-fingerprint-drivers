# Patches for ZKTeco ZK9500 (1b55:0124)

- `0001-zk9500-add-ZKTeco-ZK9500-1b55-0124-optical-driver.patch` - adds the `zk9500` optical `FpImageDevice` driver and `1b55:0124` udev hwdb autosuspend rule against upstream [libfprint](https://gitlab.freedesktop.org/libfprint/libfprint) git master (`version: '1.94.100'`), base commit `6f9479c3d55f847c1b3769f28ceb99227f9858cf` (2026-09-02, "synaptics: Add new PID 0x10b").

Apply from a libfprint checkout at that commit with `git am` or `git apply`, then build and install per [docs/BUILD.md](../../../docs/BUILD.md) and [`../README.md`](../README.md).
