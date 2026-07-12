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
MR's source branch of libfprint and build from source (see the
[`27c6:55b4`](../27c6:55b4/) entry for the general libfprint-from-source build
and PAM steps), or follow any instructions in the MR discussion.

```sh
# fetch the MR branch into a libfprint checkout, e.g.
git fetch https://gitlab.freedesktop.org/libfprint/libfprint.git \
  merge-requests/620/head:mr-620
git checkout mr-620
```

## Tested on

See the MR discussion for the current list of confirmed Dell models.

## License

Part of libfprint (LGPL-2.1). The vendor firmware blob is Broadcom-proprietary
and is not included here.
