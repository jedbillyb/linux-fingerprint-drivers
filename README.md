# linux-fingerprint-drivers

A community hub for driver code, patches, and setup notes for fingerprint
sensors that are **not yet supported in upstream
[libfprint](https://gitlab.freedesktop.org/libfprint/libfprint)**.

If your sensor shows up in `lsusb` but `fprintd-enroll` fails or the device is
unknown to libfprint, there may be a working fix here, or you can contribute one.

Browsable as a website, one page per sensor:
**<https://fprint.jedbillyb.com>**

**Check upstream first:** if your reader is on libfprint's own
[supported devices](https://fprint.freedesktop.org/supported-devices.html) list,
use your distro's libfprint. This repo is only for the ones that are not.

- [**Find your laptop by model**](docs/laptops.md) - start here if you do not know your USB ID
- [Find your device](#find-your-device)
- [Working fixes](#working-fixes)
- [In progress (unmerged upstream MRs)](#in-progress-unmerged-upstream-mrs)
- [Recently merged upstream](#recently-merged-upstream)
- [Stale (MR closed without merging)](#stale-merge-request-closed-without-merging)
- [Experimental community forks](#experimental-community-forks-not-upstream)
- [Vendor blob and non-LGPL routes](#vendor-blob-and-non-lgpl-routes-catalogued-never-hosted)
- [Claimed upstream, but unreliable](#claimed-upstream-but-unreliable)
- [No known fix yet](#no-known-fix-yet)
- [Building: **docs/BUILD.md**](docs/BUILD.md) - build, install, PAM, troubleshooting
- [Contributing](#contributing)

## Find your device

**Know your laptop but not your sensor?** Look your machine up in
**[docs/laptops.md](docs/laptops.md)**, an index of every laptop model named
anywhere in this repo or on the libfprint wiki, mapped to its USB ID and the
route that works. Adding your own model there is the most useful small
contribution you can make.

Otherwise, clone the repo and let the helper script match your hardware against
everything catalogued here:

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
| 2541:0236 (9711)     | Chipsailing CS9711      | Working | Arch (GPD Win Max 2, AYANEO 2) |
| 06cb:00ff (+00c9/00d1/00e7/0124/0169) | Synaptics Tudor MiS | Working | Arch, Fedora, Ubuntu (community routes) |
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

## Vendor blob and non-LGPL routes (catalogued, never hosted)

Some very common sensors have **no open driver at all**: the only thing that works
is a proprietary vendor driver loaded through libfprint's TOD (Touch OEM Driver)
mechanism, or a project under a license this hub cannot host.

This repo hosts **only LGPL-2.1 code**. But leaving these devices uncatalogued
just means their owners find nothing and conclude Linux cannot use their reader,
so they get entries that point at the vendor route and state the trade-offs
plainly. Nothing proprietary is mirrored here, and a pointer is not an
endorsement: read the caveats in each entry before putting a closed binary in
your authentication path.

| Device ID | Chip | Route | Entry |
|-----------|------|-------|-------|
| 27c6:550a | Goodix | Lenovo TOD blob (`libfprint-2-tod1-goodix`); ThinkPad E14/E15, ThinkBook | [entry](devices/27c6:550a/) |
| 27c6:533c | Goodix | Dell OEM TOD blob; XPS 13 9300, XPS 15 9500 | [entry](devices/27c6:533c/) |
| 04f3:0c4b | ELAN | Lenovo TOD blob (`libfprint-2-tod1-elan`); ThinkPad E14 Gen 4 | [entry](devices/04f3:0c4b/) |
| 0a5c:58xx / 586x | Broadcom | Dell/Canonical TOD blob, alongside the open MR | [entry](devices/broadcom-controlvault3/) |
| 10a5:9201 | FPC | `fingerprint-ocv`, standalone AGPL-3.0 daemon | [entry](devices/10a5:9201/) |
| 06cb:00ff family | Synaptics Tudor | relinked vendor Windows driver, *or* a fully open native driver | [entry](devices/06cb:00ff/) |

Still genuinely out of scope: sensors where nobody has published any working
route at all (those live in the [gap-map](docs/unsupported-devices.md)), and
routes we cannot verify (see [Contributing](#contributing) on the vetting bar).

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
| 138a:0097 / 009d | Validity/Synaptics VFS0097 (VCSFW) | [!626](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/626), [!579](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/579), [!619](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/619) | !626 is the active continuation of !579; also covers 0090 + 06cb:009a |
| 138a:00ab | Validity VCSFW 0x969/0xd51 | [!626](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/626) | hardware-validated; HP ZBook Studio x360 G5 |
| 06cb:00cb | Validity VCSFW 0x969 | [!626](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/626) | hardware-validated; HP Pavilion x360 14-dh |
| 06cb:00b7 | Validity VCSFW 0xd51 | [!626](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/626) | registered, untested; HP G6 series |
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
| 2808:6553 | FocalTech FT9365 ESS ([not the capture function on dual-function FT9201 modules](devices/2808:6553/README.md#caveat-on-dual-function-ft9201-modules)) | [!554](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/554) | 2026-06-18 |
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


## Claimed upstream, but unreliable

libfprint listing your sensor as supported does not always mean it works. These
have in-tree drivers that fail in practice, with open MRs that fix them. If your
reader is *detected* but you cannot finish an enrollment, start here.

| Device ID | Chip | Problem | Fix MR | Entry |
|-----------|------|---------|--------|-------|
| 04f3:0c28 (0c0x-0c4x family) | ELAN image sensors | enroll fails every second capture; thresholds and swipe-mode assumptions wrong for the hardware | [!217](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/217), [!530](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/530) | [entry](devices/04f3:0c28/) |
| 1c7a:0570 (0571) | EgisTec egis0570 | calibration not implemented, erratic captures | [!548](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/548) | [entry](devices/1c7a:0570/) |
| 147e:1002 and upektc/upeksonly | UPEK swipe sensors | 144x384 captures yield too few minutiae to match reliably | [!576](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/576) | [entry](devices/147e:1002/) |
| 1c7a:05ae, 1c7a:9201 | EgisTec etu905 | no firmware template update after verify | [!610](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/610) | - |

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

**Hosting vs cataloguing.** Code and patches in this repo are LGPL-2.1 only.
Cataloguing is broader: a device entry may point at a proprietary TOD blob or a
differently-licensed project when that is the only thing that works, as long as
the entry says so plainly and mirrors none of it.

**Vetting bar.** There are many small per-device fingerprint repos on GitHub, and
a fair number are abandoned, unlicensed, or generated. An entry gets added when
the route can be checked: real driver code, a license, and some evidence it
worked on hardware. Unverifiable leads belong in an issue, not in `devices/`.

Where a fix belongs upstream, please also push it there: this hub exists to make
unmerged work findable, not to replace
[libfprint](https://gitlab.freedesktop.org/libfprint/libfprint). Entries whose
merge requests land upstream get moved to the merged table and eventually
dropped.

## License

All driver code and patches **hosted** here are derived from libfprint and are
licensed under **LGPL-2.1**. See [LICENSE](LICENSE). Contributed code must be
LGPL-2.1-compatible.

Device entries may *link* to routes under other licenses, including proprietary
vendor drivers, where that is the only thing that works for a sensor. Those
entries say so explicitly and mirror no code. See
[Vendor blob and non-LGPL routes](#vendor-blob-and-non-lgpl-routes-catalogued-never-hosted).
