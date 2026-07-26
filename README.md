# linux-fingerprint-drivers

A community hub for driver code, patches, and setup notes for fingerprint
sensors that are **not yet supported in upstream
[libfprint](https://gitlab.freedesktop.org/libfprint/libfprint)**.

If your sensor shows up in `lsusb` but `fprintd-enroll` fails or the device is
unknown to libfprint, there may be a working fix here, or you can contribute one.

**Check upstream first:** if your reader is on libfprint's own
[supported devices](https://fprint.freedesktop.org/supported-devices.html) list,
use your distro's libfprint. This repo is only for the ones that are not.

- [Find your device](#find-your-device)
- [Working fixes](#working-fixes)
- [In progress (unmerged upstream MRs)](#in-progress-unmerged-upstream-mrs)
- [Recently merged upstream](#recently-merged-upstream)
- [Stale (MR closed without merging)](#stale-merge-request-closed-without-merging)
- [Experimental community forks](#experimental-community-forks-not-upstream)
- [No known fix yet](#no-known-fix-yet)
- [Building: **docs/BUILD.md**](docs/BUILD.md) - build, install, PAM, troubleshooting
- [Contributing](#contributing)

## Find your device

Clone the repo and let the helper script match your hardware against everything
catalogued here:

```sh
git clone https://github.com/jedbillyb/linux-fingerprint-drivers.git
cd linux-fingerprint-drivers
./tools/detect.sh              # or: ./tools/detect.sh 27c6:55b4
```

It scans `lsusb` for likely readers and tells you, per device, whether there is
an entry here, whether it is on the known-unsupported list, or whether it is
unknown to this repo entirely.

Doing it by hand: run `lsusb` and find the reader:

```
$ lsusb
...
Bus 003 Device 002: ID 27c6:55b4 Shenzhen Goodix Technology Co.,Ltd. FingerPrint
...
```

The `27c6:55b4` part is the USB ID (`vendor:product`), and it is the key this
repo is organised by: see [`devices/27c6:55b4/`](devices/27c6:55b4/). If nothing
is obviously a reader, compare against the known sensor vendors: Goodix `27c6`,
Synaptics/Validity `06cb` and `138a`, ELAN `04f3`, FocalTech `2808`, FPC `10a5`,
Broadcom `0a5c`, EgisTec `1c7a`. Many newer sensors are on SPI or I2C and never
appear in `lsusb` at all.

## Working fixes

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
caveats), **WIP** (in progress). Statuses only move when someone reports back,
so please open a [device report](.github/ISSUE_TEMPLATE/device-report.yml) with
your distro and hardware either way.

Every entry needs libfprint built from source. The build, install, PAM, package
pinning, troubleshooting and revert steps are the same for all of them and live
in **[docs/BUILD.md](docs/BUILD.md)**; each device entry covers only what is
specific to that sensor.

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

## In progress (unmerged upstream MRs)

Drivers that have been submitted to the **official libfprint project** but are
**not merged yet**, so they are not in any released libfprint. Each has an entry
under [`devices/`](devices/) with the merge-request link and build notes. Status
changes to Working here once someone confirms it, and the row moves once the MR
lands upstream.

MR states were last verified against GitLab on **2026-07-26**; the merge request
itself is always the authority.

| Device ID | Chip / sensor | MR | Notes |
|-----------|---------------|----|-------|
| 147e:1002 | UPEK Touchstrip (upeksonly) | [!585](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/585) | Draft |
| 0a5c:xxxx (Dell) | Broadcom ControlVault3 (fp + NFC) | [!620](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/620) | Dell family; needs vendor firmware; see [entry](devices/broadcom-controlvault3/) |
| 138a:0097 / 009d | Validity/Synaptics VFS0097 (VCSFW) | [!579](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/579), [!619](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/619) | native driver; also covers 0090 + 06cb:009a |
| 2808:c652 | FocalTech FT9362 (match-on-host) | [!588](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/588) | |
| 2808:9338 / 93a9 | FocalTech FT9201 | [!572](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/572) | |
| 10a5:9200 | FPC1022 (FPC Disum) | [!570](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/570) | |
| 10a5:9924 | FPC match-on-host (Honor) | [!611](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/611) | |
| 04e8:7305 | Samsung 7305 | [!586](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/586) | |
| 04e8:730b | Samsung 730B (image) | [!556](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/556) | |
| 1c7a:0576 | EgisTec 0576 | [!571](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/571) | |
| 1c7a:0575 | EgisTec EGIS0575 (swipe) | [!357](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/357) | Needs work |
| 298d:2033 | NextBiometrics NB-2033-U | [!574](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/574) | |
| crfpmoc (cros_ec) | Chromium OS EC FPMCU | [!512](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/512) | not USB |
| mafp8800 (SPI) | Microarray MAFP8800 | [!580](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/580) | not USB (SPI) |

### Recently merged upstream

These were WIP here but their merge requests have since **merged into libfprint
git master** (2026-06/07). They will be in the next libfprint release; build from
git to get them now. Entries are kept for people still on an older libfprint.

| Device ID | Chip / sensor | MR | Merged |
|-----------|---------------|----|--------|
| 2808:6553 | FocalTech FT9365 ESS | [!554](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/554) | 2026-06-18 |
| 04f3:0c9c | ELAN ARM-M4 (0c9c) | [!568](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/568) | 2026-06-18 |
| 3274:8012 | Microarray match-on-chip | [!492](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/492) | 2026-06-18 |
| 298d:2020 | NextBiometrics NB-2020-U | [!569](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/569) | 2026-07-02 |

### Stale (merge request closed without merging)

Entries kept as leads for anyone wanting to pick the reverse-engineering back up.

| Device ID | Chip / sensor | MR | State |
|-----------|---------------|----|-------|
| [04f3:0c8e](devices/04f3:0c8e/) | ELAN elanmoc2 | [!560](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/560) | Closed 2026-06-22; no maintained upstream work |
| [04f3:310d](devices/04f3:310d/) | ELAN ELAN7006 | [!383](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/383) | Closed; the draft never enrolled or verified |

### Experimental community forks (not upstream)

Drivers from community forks rather than upstream merge requests. These are not
in libfprint and may be unstable; see each device entry for details.

| Device ID | Chip / sensor | Source | Notes |
|-----------|---------------|--------|-------|
| 27c6:521d (538d) | Goodix 521d/538d | [goodix-fp-linux-dev](https://github.com/goodix-fp-linux-dev) | Works via AUR `libfprint-goodix-521d` |
| 27c6:5110 + family | Goodix (newer) | [goodix-fp-linux-dev/libfprint](https://github.com/goodix-fp-linux-dev/libfprint) | **Experimental, not for daily use** |


## No known fix yet

115 more USB sensors are on the libfprint wiki's unsupported list with no
working driver here or upstream. They are catalogued, with any known
reverse-engineering leads, in
**[docs/unsupported-devices.md](docs/unsupported-devices.md)** - the contributor
gap-map. If you own one of those, a protocol dump or a driver is very welcome.

SPI/I2C sensors (ELAN7001/7002/079C, GXFP5187/51B7, GDIX51C0, fpc1020, ...) are
also largely unsupported and never appear in `lsusb`; see the wiki's SPI Devices
section.

## Contributing

New device entries, status reports, and corrections are all welcome. See
[CONTRIBUTING.md](CONTRIBUTING.md) for the folder layout, required files,
attribution, and license rules, and run `python3 tools/check-repo.py` before
opening a PR.

Two things are worth as much as a driver: a **report** that an entry works (or
stopped working) on your distro, and a **protocol dump** for anything in the
[gap-map](docs/unsupported-devices.md).

Where a fix belongs upstream, please also push it there: this hub exists to make
unmerged work findable, not to replace
[libfprint](https://gitlab.freedesktop.org/libfprint/libfprint). Entries whose
merge requests land upstream get moved to the merged table and eventually
dropped.

## License

All driver code and patches here are derived from libfprint and are licensed
under **LGPL-2.1**. See [LICENSE](LICENSE). Contributions must be
LGPL-2.1-compatible.
