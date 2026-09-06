# ELAN ARM-M4 (USB 04f3:0c80)

**Status: Partial - enroll and verify work with an experimental local patch, but clearing sensor storage still times out and re-enrolling wipes every stored print.**

ELAN "ARM-M4" match-on-chip fingerprint reader, reported in the Surface Laptop
Go 2.

## What was broken

The USB ID is not in any `elanmoc2` ID table, upstream or in the community
forks, so a stock install never binds a driver to it. `fprintd-enroll` fails
with `NoSuchDevice` and the daemon logs:

```text
No driver found for USB device 04F3:0C80
```

## What the fix does

Patches Davide Depau's `elanmoc2` branch to add the sensor and three quirks it
needs. Only one machine has been tested, and the erase path is not fully
solved, so treat this as a lead rather than a finished driver.

- Adds `04f3:0c80` to the `elanmoc2` ID table.
- `ELANMOC2_QUIRK_USE_EP83` routes identify and enroll replies to endpoint
  `0x83` instead of `0x84`.
- `ELANMOC2_QUIRK_NO_DELETE_BY_ID` skips per-finger deletion during
  re-enrollment and falls through to the whole-sensor wipe. **This is not
  selective deletion: re-enrolling can remove every stored print.**
- `ELANMOC2_QUIRK_WIPE_ACK` reads a device-specific two-byte reply after the
  `40 ff 99` erase command, then waits five seconds before the next state.
- Clears `in_flight_cmd` on transfer error and guards overlapping commands and
  close-time cancellation. These stop an earlier assertion, but dropping
  commands is a workaround and the cancellation lifecycle still needs review.

The EP83 and no-delete-by-ID leads came from the same quirk pair working on a
Surface Laptop Go 1 (`04f3:0c5a`) on Fedora.

## Known limitation

Clearing storage before the first enrollment still fails:

```text
Erase acknowledgement received; waiting for sensor
SSM CLEAR_STORAGE_NUM_STATES failed in state 1 with error: transfer timed out
Failed to clear storage before first enrollment: transfer timed out
```

fprintd carries on regardless: the following count/identify succeeds, reports
zero stored fingers, and enrollment completes. It is not established whether
recovery comes from the acknowledgement handling, the added delay, or both.
Cold boot, suspend/resume, repeated delete and re-enroll, and multi-finger
reliability are all untested.

## Build and install

The patch applies to Davide Depau's `libfprint` fork at commit
`11f0316d069cc90c154c8cb0e46478388c5e2a74` ("WIP add 0c7c"), **not** to the
current `xerootg` branch, where quirk names and surrounding code differ. See
`patches/README.md` for the base commit and
[docs/BUILD.md](../../docs/BUILD.md) for the shared build, install and PAM
steps. The deltas for this sensor:

```sh
git clone https://gitlab.freedesktop.org/Depau/libfprint.git
cd libfprint
git checkout 11f0316d069cc90c154c8cb0e46478388c5e2a74
git apply /path/to/patches/0001-elanmoc2-add-04f3-0c80.patch

meson setup build-slg2 --prefix=/usr --libdir=lib \
  -Ddoc=false -Dinstalled-tests=false -Ddrivers=elanmoc2
meson compile -C build-slg2
sudo meson install -C build-slg2 --no-rebuild
sudo systemctl restart fprintd
```

On Arch the GLib development tools must be present, `glib-mkenums` in
particular. Reproduction from a fresh checkout has not been independently
tested.

> This replaces your distro's libfprint. Keep a way to reinstall the stock
> package, which will also silently undo this driver on the next update.

## Tested on

- Omarchy (Arch), kernel 7.1.9-arch1-2, Surface Laptop Go 2. Enroll and verify
  both succeed, verify still matches after restarting fprintd, and fingerprint
  authentication for `sudo` was confirmed working. Single reporter, single
  machine.
- Originally reported as `NoSuchDevice` on the same machine before the patch.
