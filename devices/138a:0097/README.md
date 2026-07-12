# Validity/Synaptics VFS0097 (VCSFW) (USB 138a:0097, 138a:009d)

**Status: WIP (unmerged upstream MR)**

Device ID(s): `138a:0097`, `138a:009d` (and the wider VCSFW family, which also
covers `138a:0090` and `06cb:009a`).

These Validity/Synaptics sensors speak the **VCSFW** protocol (not the BMKT
protocol the in-tree `synaptics` driver assumes), so upstream libfprint has
historically mis-claimed them without working enroll/verify. Found in ThinkPad
T480/T480s/T580/X1 Carbon Gen6 and many other laptops.

This is a driver submitted to the **official libfprint project** but **not merged
yet**, tracked here so people with these sensors can find and build the work in
progress.

## Upstream merge requests

- libfprint MR !579 (native VCSFW driver):
  https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/579
  Author: @lewohart
- libfprint MR !619 (straight port of @3v1n0's TOD vfs0090/vfs0097 driver):
  https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/619
  Author: Willem Mulder (@14mRh4X0r)

## What it does

MR !579 is a from-scratch native driver: VCSFW command/response over bulk
endpoints, full TLS 1.2 session with the sensor (ECDH, AES-CBC, flash-stored
cert/key parsing), Windows-Hello-compatible pairing, firmware-extension upload,
multi-stage enroll (~8-9 stages), match-on-chip verify/identify, and per-print
delete + storage clear. It supersedes the following IDs previously (incorrectly)
claimed by the BMKT `synaptics` driver:

| VID:PID     | Device                          |
|-------------|---------------------------------|
| `138a:0090` | Validity VFS0090                |
| `138a:0097` | Validity VFS0097                |
| `06cb:009a` | Synaptics Metallica MIS Touch   |
| `138a:009d` | Validity VFS0097                |

MR !619 is an alternative: a direct upstreaming of @3v1n0's out-of-tree
`libfprint-tod-vfs0090` driver (confirmed working with a Validity 0090; lacks
capture support for vfs0097).

## Related entries

- [`138a:0090`](../138a:0090/) - VFS0090, already working via the established
  out-of-tree route; !579/!619 aim to bring it (and 0097) natively upstream.
- [`06cb:009a`](../06cb:009a/) - currently handled by python-validity; !579 is a
  native libfprint alternative.

## How to use it

The code lives in the merge requests, not in this repo. Pick one MR, check out
its source branch of libfprint, and build from source (see the
[`27c6:55b4`](../27c6:55b4/) entry for the general libfprint-from-source build
and PAM steps).

```sh
# native VCSFW driver (MR !579)
git fetch https://gitlab.freedesktop.org/libfprint/libfprint.git \
  merge-requests/579/head:mr-579
git checkout mr-579
```

## Tested on

Reported on ThinkPad T480/T480s/T580/X1 Carbon Gen6; see the MR discussions for
current confirmations.

## License

Part of libfprint (LGPL-2.1).
