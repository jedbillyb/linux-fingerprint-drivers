# Synaptics "Viper" via python-validity (USB 06cb:008a)

**Status: Working via python-validity (userspace daemon, not a libfprint driver).**

Synaptics/Validity "Viper" fingerprint readers (ASIC 57K0 FM-154-124, ROM 6.20).
Found primarily in Toshiba / Dynabook business laptops (Tecra X40-D, Portégé X30-D).

## What was broken

The `06cb:008a` sensor is strictly Match-on-Host. `GetFirmwareInfo (0x4302)`
returns `0x04af` (no firmware detected), and Match-on-Chip commands (`0x68`, `0x5e`)
fail with `0401` (invalid command). No `.xpfwext` firmware extension exists or is used.
Additionally, writing templates directly to the sensor's SPI flash table triggers
USB bus contention and device disconnection.

## What the fix does (architecture is different)

`python-validity` is **not a libfprint driver**. It is a reverse-engineered
**userspace daemon** that communicates directly with the sensor over USB via DBus.
It registers itself with the **open-fprintd** service so that standard `fprintd`
clients and PAM modules work seamlessly.

The `06cb:008a` implementation adds:
- Passive interrupt acquisition on EP `0x83` streaming full 56×144 8-bit grayscale matrix frames (8,064 bytes).
- 2D Phase Correlation matching (`numpy.fft.fft2`) with 2D Hann window filtering (eliminating edge boundary step artifacts) and an angular tilt search (`[-12° .. +12°]`).
- Host-side template persistence in `/var/lib/python-validity/templates/`.

So the stack is: `python-validity` (device driver daemon) -> `open-fprintd`
(fprintd-compatible DBus service) -> `fprintd-clients` / `pam_fprintd`.

Upstream pull requests:
- python-validity: [PR #293](https://github.com/uunicorn/python-validity/pull/293)
- open-fprintd: [PR #31](https://github.com/uunicorn/open-fprintd/pull/31)

## Install

Prebuilt packages and source fork are maintained at:
- [the-muzammilali/python-validity](https://github.com/the-muzammilali/python-validity)
- [Releases](https://github.com/the-muzammilali/python-validity/releases/tag/v0.16-viper1)

### Quick install (.deb)

```sh
sudo apt update
sudo apt install -y python3-usb python3-cryptography python3-numpy python3-pil python3-yaml python3-dbus python3-gi fprintd libpam-fprintd
sudo dpkg -i open-fprintd_0.6-viper1_all.deb python3-validity_0.16-viper1_all.deb

fprintd-enroll
fprintd-verify
```

## PAM setup

Once open-fprintd is running, configure PAM exactly as for normal fprintd
(distro helper or `auth sufficient pam_fprintd.so`); see
[docs/BUILD.md](../../docs/BUILD.md#6-pam-setup-login--sudo--lock-screen). The build sections of that
guide do not apply here, since python-validity is packaged rather than built.

## Tested on

- Ubuntu 24.04 LTS (Toshiba Tecra X40-D)

## License note

python-validity is MIT-licensed. It is listed here as the canonical working fix
even though it is a userspace daemon rather than a libfprint driver.
