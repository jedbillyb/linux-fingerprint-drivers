# Patches for Blestech Betterlife btlfp (347d:0302, 347d:0304)

- `0001-betterlife347d-add-Blestech-Betterlife-347d-0302-and.patch` - adds `betterlife347d_moc` (`347d:0302` match-on-chip) and `betterlife347d` (`347d:0304` match-on-host), OpenSSL 3 SM2/SM3/SM4 session framing, and udev hwdb autosuspend entries against upstream [libfprint](https://gitlab.freedesktop.org/libfprint/libfprint) git master (`version: '1.94.100'`), base commit `6f9479c3d55f847c1b3769f28ceb99227f9858cf` (2026-09-02, "synaptics: Add new PID 0x10b").

Apply with `git am` or `git apply` and build per [docs/BUILD.md](../../../docs/BUILD.md) (needs `libssl-dev` / `openssl-devel` >= 3.0).

Note: `347d:0302` matches on the sensor MCU and works at full accuracy with this upstream patch. `347d:0304` compiles with an NBIS fallback here, but 96x112 images match much better on a SIGFM tree; see [`../README.md`](../README.md) for the SIGFM build route.
