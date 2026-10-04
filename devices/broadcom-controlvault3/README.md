# Broadcom ControlVault3 (Dell)

**Status: WIP (unmerged upstream MR)**

Device ID(s): Broadcom `0a5c` family (Dell ControlVault3). The MR does not pin a
single product ID; these are the combined fingerprint + NFC security controllers
Dell ships across many Latitude, Precision, and XPS models. Match your `0a5c:xxxx`
ID from `lsusb` against the device table in the merge request.

This is a driver that has been submitted to the **official libfprint project**
but is **not merged yet**, so it is not in any released libfprint. Tracked here so
people with a Dell ControlVault3 reader can find and build the work in progress.

## Upstream merge request

- libfprint MR !620: https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/620
- Author: Erik Håkansson (@erikhakan)

## What it does

Adds a native driver for Broadcom ControlVault3 devices used on a large number
of Dell laptops. These are dual fingerprint + NFC controllers with on-device
storage (delete is supported; list/clear are firmware-gated behind a management
mode and are not available, so the driver advertises `FP_DEVICE_FEATURE_STORAGE`
manually).

## Firmware note (important)

Dell/Broadcom ship a proprietary firmware blob (flashed by the vendor Windows /
Ubuntu driver) that is **not** redistributed with this driver. Running very old
sensor firmware has known security implications (see the ReVault advisory:
https://blog.talosintelligence.com/revault-when-your-soc-turns-against-you/), so
the driver gates against too-old firmware with a warning; the threshold is
configurable in the driver source. Upgrading firmware currently means installing
Dell's proprietary driver stack.

## How to use it

The code lives in the merge request, not in this repo. To try it, check out the
MR's source branch of libfprint and build from source (see
[docs/BUILD.md](../../docs/BUILD.md) for the shared build, install, PAM and
troubleshooting steps), or follow any instructions in the MR discussion.

```sh
# fetch the MR branch into a libfprint checkout, e.g.
git fetch https://gitlab.freedesktop.org/libfprint/libfprint.git \
  merge-requests/620/head:mr-620
git checkout mr-620
```

## Tested on

See the MR discussion for the current list of confirmed Dell models.

## Reports

- **Dell Precision 7560, `0a5c:5842`, MR !620 build, not working**
  ([#27](https://github.com/jedbillyb/linux-fingerprint-drivers/issues/27), 2026-10-01).
  The driver probes and opens the device, and the firmware (AAI `00515015`,
  SBI 234) is above the MR's minimums. Enrollment fails before any finger
  capture: `START_ENROLL (0x8a)` succeeds, then the first `GET_CHALLENGE (0x66)`
  returns status `0x75`, which is not in the MR's status table. Under fprintd
  the same `0x75` appears earlier, on the identify fprintd runs before enrolling;
  a direct libfprint `enroll_sync` that skips it fails the same way, so this is
  not just an identify quirk. The vendor TOD driver (`5.15.377_5.15.021.0`) also
  fails to enroll on this unit.
  The MR author [looked into `0x75`](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/620#note_3693300)
  (2026-10-03): the CV3 firmware checks its hardware-discovery flags on
  `GET_CHALLENGE` and returns `0x75` when it did not find or could not
  initialise the fingerprint sensor at boot. So this is a fault on this unit
  (cabling, damaged sensor or a bad earlier flash), not a driver bug. Untested
  recovery ideas: force-reflashing with
  [broadcom-cv3-fwupdater](https://github.com/erikhakansson/broadcom-cv3-fwupdater),
  or Dell's Windows driver. Both carry flash risk.
- **Dell Precision 3490, `0a5c:5865` (ControlVault3 Plus), not working**
  ([#28](https://github.com/jedbillyb/linux-fingerprint-drivers/issues/28), 2026-09-26).
  Vendor TOD blob `brcm_linux_fp_6.4.372_6.4.062.0` detects the reader and
  upgrades its firmware (AAI 6.0.56.0 to 6.4.62.0), but enrollment fails at the
  first stage every time with `Device status = (-99)`. The older 6.1.155 blob
  fails the same way. The sensor behind the ControlVault is a Goodix GF5288, and
  Ubuntu's certification page for this model says the reader is not supported.
  A matching PID is not enough to assume a CV3+ machine will work: the PID names
  the controller, not the sensor behind it.
  USB notes from the report, for a future CV3+ port of MR !620: same transport
  as CV3 (commands on EP1 OUT, an 8-byte `{status, len}` interrupt on EP5 IN,
  response on EP1 IN, `03 00 00 00 00 00 00 00` = finger on sensor), but the
  frames start `08 00 00 00` and the payload looks encrypted, where CV3 uses a
  version-1 header and plaintext TLVs.

## License

Part of libfprint (LGPL-2.1). The vendor firmware blob is Broadcom-proprietary
and is not included here.

## Vendor TOD route (works today, proprietary)

While MR !620 is unmerged, the working route on these Dell machines is Broadcom's
proprietary driver loaded through libfprint TOD. Nothing from it is hosted here.

| Distro | Route |
|--------|-------|
| Ubuntu | Dell OEM package `libfprint-2-tod1-broadcom` ([Launchpad source](https://git.launchpad.net/~oem-solutions-engineers/libfprint-2-tod1-broadcom/+git/libfprint-2-tod1-broadcom/)) |
| Arch | AUR `libfprint-2-tod1-broadcom` (Latitude 7300 class), or `libfprint-2-tod1-broadcom-cv3plus` for **ControlVault3 Plus** (`0a5c:586*`), sourced from [Broadcom's artifactory](https://packages.broadcom.com/artifactory/dell-controlvault-drivers/) |
| Other | Extract Dell's `.deb` and install the TOD module against a TOD-enabled libfprint |

You still need the ControlVault firmware described above. The blob is closed
source, x86-64 only, and tied to a libfprint TOD ABI; keep password auth working.
