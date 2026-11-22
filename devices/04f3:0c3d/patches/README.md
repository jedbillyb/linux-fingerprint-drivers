# Patches for ELAN 04f3:0c3d (elanpress)

Both patches apply in order to upstream libfprint at commit
`6f9479c3d55f847c1b3769f28ceb99227f9858cf` (v1.94.100 + 10):

```sh
git clone https://gitlab.freedesktop.org/libfprint/libfprint.git
cd libfprint
git checkout 6f9479c3d55f847c1b3769f28ceb99227f9858cf
patch -Np1 -i 0001-elanpress-driver.patch
patch -Np1 -i 0002-elanpress-0c3d.patch
```

- `0001-elanpress-driver.patch` adds the `elanpress` press driver from
  [filip-rs/libfprint](https://github.com/filip-rs/libfprint) (branch
  `elanpress`) and moves `0c4f`, `0c63` and `0c6e` to it. It is the patch
  Omarchy carries for those press sensors.
- `0002-elanpress-0c3d.patch` adds `0x0c3d` to `elanpress_id_table` with the
  `ELANPRESS_0C3D` flag, uses `ELANPRESS_TOUCH_PIXEL_DELTA_WEAK` (600) for it,
  removes it from the swipe driver and moves its `autosuspend.hwdb` line to the
  elanpress section. Other PIDs keep the default threshold of 1200.

The same pair is wired into an Arch `PKGBUILD` at
https://github.com/iverlaek/libfprint-elanpress-0c3d. MR !654 takes a different,
larger approach to the same sensor and is not required for these patches.
