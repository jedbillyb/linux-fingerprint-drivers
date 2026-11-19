# ELAN ARM-M4 (USB 04f3:0c77)

**Status: Partial - enroll and verify work through fprintd with a patched elanmoc2 driver; a finger resting on the sensor while it is opened can make it stop answering for about a minute.**

ELAN "ARM-M4" match-on-chip fingerprint reader, found in ASUS ExpertBook
models. Requested upstream in libfprint
[#447](https://gitlab.freedesktop.org/libfprint/libfprint/-/issues/447),
[#510](https://gitlab.freedesktop.org/libfprint/libfprint/-/issues/510) and
[#692](https://gitlab.freedesktop.org/libfprint/libfprint/-/issues/692).

## What was broken

The USB ID is in no libfprint driver, so `fprintd-enroll` fails with
`NoSuchDevice`. Adding the ID to an existing upstream driver does not help:

- With the `elan` image driver the device initialises, but the capture command
  is never answered (reported in #447 and #510).
- With the `elanmoc` driver the device opens, but the first step of an
  enrollment, the re-enroll check `40 ff 22`, is never answered.

## What the fix does

Ports Davide Depau's `elanmoc2` driver to current upstream libfprint, adds
`04f3:0c77`, and changes what this sensor needed:

- Builds the print from 15 samples instead of 8. With 8 the sensor accepted the
  enrollment, but the stored print never matched.
- Tolerates a stray packet. With a finger resting on the sensor while the
  device is opened, the first query is answered with six zero bytes; the driver
  drops them and asks again.
- No longer sends an abort command every time the device is closed.
- Never falls back to wiping the whole sensor when deleting one print fails.

It also fixes bugs that are not specific to this sensor: wrong reporting of
retries and "no match" in verify (with a double free), a receive timeout while
waiting for a finger, and a crash when closing right after a cancellation.

The protocol findings are written up in the source repository, see `CREDITS`.

## Known limitation

In 2 of 11 cases where the six zero bytes appeared, the sensor did not answer
the repeated query either. The operation failed after a 10 second timeout, and
the USB reset of the next open left the sensor dead on the bus for 60-75
seconds. It recovered by itself every time. This only happened with a finger
resting on the sensor while the device was opened; normal touches matched in
38 of 38 runs.

The sensor also rejects touches that cover too little of it, about 1 in 6
after some practice; fprintd asks for another touch.

Listing stored prints and deleting a single print from fprintd are not
implemented. Clearing the sensor and re-enrolling a finger both work.

## Build and install

The patch applies to upstream libfprint at commit
`6f9479c3d55f847c1b3769f28ceb99227f9858cf` (v1.94.100 + 10). See
`patches/README.md` for the base and [docs/BUILD.md](../../docs/BUILD.md) for
the shared build, install and PAM steps. The deltas for this sensor:

```sh
git clone https://gitlab.freedesktop.org/libfprint/libfprint.git
cd libfprint
git checkout 6f9479c3d55f847c1b3769f28ceb99227f9858cf
patch -Np1 -i /path/to/patches/0001-elanmoc2-driver-with-04f3-0c77.patch
```

On Arch and Omarchy the source repository has a `PKGBUILD` that does this and
builds a package. It is named `libfprint-git` with epoch 2, so that Omarchy's
`omarchy-setup-security-fingerprint` accepts it and a system update does not
replace it.

Enrolling takes 15 good touches. Lift the finger between touches, and do not
rest it on the sensor while fprintd starts.

## Tested on

- Omarchy (Arch), kernel 7.2.15, fprintd 1.94.5, ASUS ExpertBook B9403CVAR,
  reader firmware 0x316. Enroll and verify through fprintd, clearing the
  sensor, Omarchy's fingerprint setup, and unlocking the lock screen after
  suspend (s2idle) and after hibernate. Single reporter, single machine.
- The ExpertBook B5 Flip and B7 Flip are reported to have the same reader and
  have not been tested with this patch.
