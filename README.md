# linux-fingerprint-drivers

A community hub for driver code, patches, and setup notes for fingerprint
sensors that are **not yet supported in upstream
[libfprint](https://gitlab.freedesktop.org/libfprint/libfprint)**.

If your sensor shows up in `lsusb` but `fprintd-enroll` fails or the device is
unknown to libfprint, there may be a working fix here, or you can contribute one.

## Find your device ID

Run `lsusb` and look for your fingerprint reader:

```
$ lsusb
...
Bus 003 Device 002: ID 27c6:55b4 Shenzhen Goodix Technology Co.,Ltd. FingerPrint
...
```

The `27c6:55b4` part is the USB ID (`vendor:product`). That is the key used to
organise this repo: see `devices/27c6:55b4/`.

If you are not sure which entry is the reader, unplug/replug is not an option on
laptops, so compare `lsusb` output against the known vendors (Goodix `27c6`,
Synaptics `06cb`, Elan `04f3`, etc.).

## Supported devices

| Device ID            | Chip                    | Status  | Distros tested              |
|----------------------|-------------------------|---------|-----------------------------|
| 27c6:55b4            | Goodix GF3268           | Working | Void Linux                  |
| 27c6:5385 (5335/5395)| Goodix HTK32            | Working | Arch, Fedora, Ubuntu/Debian |
| 04f3:0c4c (0c00)     | ELAN match-on-chip      | Working | Debian/Ubuntu               |
| 138a:0090 (0097)     | Validity/Synaptics VFS0090 | Working | Ubuntu, Arch, Fedora, NixOS |
| 06cb:009a (138a:009d)| Synaptics Prometheus    | Working | Ubuntu, Arch, Fedora         |
| 04f3:0c6c            | ELAN Match-on-Chip 2    | Working | Ubuntu/Debian, Fedora, Arch |
| 10a5:9800            | FPC fpcmoh (match-on-host) | Working | Fedora, Arch              |
| 2808:9e65            | FocalTech               | Partial | Undocumented (unconfirmed)  |

Status legend: **Working** (enroll + verify reliable), **Partial** (works with
caveats), **WIP** (in progress).

Note: `06cb:009a` (Synaptics Prometheus) is handled by **python-validity**, a
userspace driver daemon that plugs into `fprintd` via `open-fprintd`, rather than
a libfprint driver. See its [entry](devices/06cb:009a/) for the different stack.

### Out of scope

Some sensors only have fixes that do not fit this hub's LGPL-2.1 scope, so they
are not catalogued here as device entries:

- **27c6:550a** (Goodix) - works via Lenovo's proprietary `libfprint-2-tod-goodix`
  TOD binary blob, not open driver code.
- **10a5:9201** (FPC) - the `fingerprint-ocv` driver is a standalone AGPL-3.0
  project, not an LGPL-2.1 libfprint driver.
- Proprietary vendor blobs in general (e.g. various FocalTech `2808:a658` ASUS
  drivers).

## Contributing

New device entries are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the
folder layout, required files, attribution, and license rules.

## License

All driver code and patches here are derived from libfprint and are licensed
under **LGPL-2.1**. See [LICENSE](LICENSE). Contributions must be
LGPL-2.1-compatible.
