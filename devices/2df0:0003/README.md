# CanvasBio CB2000 (USB 2df0:0003)

**Status: Working via community drivers, none of them upstream; the sibling ID `2df0:0007` is not covered by any of them and stalls on contact. On the upstream Realtek driver it enrolls and matches on the chip; an experimental community patch gets it to login and `sudo`, but its verify accepts any finger stored on the chip.**

CanvasBio CB2000, the fingerprint reader in the Samsung Galaxy Book2 360 and
Book3 360 generation. Upstream libfprint has never supported it and there is no
merge request for `2df0` in any state, but four independent people have
reverse-engineered it from the Samsung Windows driver, and at least two report
daily use for login and `sudo`.

## What was broken

The sensor is unknown to stock libfprint, so nothing binds to it and
`fprintd-enroll` reports no devices.

Worse, it does not fit libfprint's normal image path even once you can talk to
it. The CB2000 delivers an 80x64 greyscale image covering roughly 5x4 mm of
fingertip. NBIS/bozorth3 wants somewhere around 20 minutiae to match; on frames
this small it typically finds 0 to 3. Neither adjusting `ppmm` nor upscaling
helps, because the minutiae are not in the frame to begin with. Every working
driver below therefore derives from `FpDevice` rather than `FpImageDevice` and
brings its own matcher, building a template from many frames instead of one.

## The drivers

None of these is upstream, none is packaged by a distro, and all of them
replace or extend your libfprint. Read the source before installing.

| Project | Approach | Licence | Notes |
|---------|----------|---------|-------|
| [kpagnussat/canvasbio-cb2000](https://github.com/kpagnussat/canvasbio-cb2000) | SIGFM feature matching, multi-capture mosaic template | LGPL-2.1 | Most actively developed. `R2.5` snapshot, 15 enroll stages, requires OpenCV, disables libfprint's virtual thermal shutdown for this device. Use the repo: an older single-file [GitLab snippet](https://gitlab.com/-/snippets/4931207) ("V44", February) predates it and its current matcher, was never a release, and its author asks that it be disregarded |
| [LennartArnholdt/libfprint-tod-cb2000](https://github.com/LennartArnholdt/libfprint-tod-cb2000) | SIFT feature matching, 30-frame template | LGPL-2.1-or-later AND MIT | Reports ~83% single-touch genuine acceptance and 0 false accepts in 1080 comparisons, measured across separate sessions on one device. PAM setup documented |
| [latex/canvasbio-cb2000-linux-driver](https://github.com/latex/canvasbio-cb2000-linux-driver) | Standalone driver plus CLI tooling (`cb2000_demo`, `fpsudo`) | MIT | Ships an `install.sh`. Developed on a Book3 360 (730QFG) |
| [rfocosi/libfprint](https://github.com/rfocosi/libfprint) | libfprint fork carrying a CB2000 driver | none stated | Whole-library fork rather than a patch |
| [vgperess/libfprint-canvasbio-cb2000](https://github.com/vgperess/libfprint-canvasbio-cb2000) | - | none stated | Earliest of the set, quiet since 2025 |

**On licensing:** this repo hosts none of the above, it points at them. The MIT
and unlicensed ones are noted so you can make your own call before mixing code
into an LGPL-2.1 library.

## Do not use these on 2df0:0007

`2df0:0007` is a different part in the same family, reported in the Samsung
Galaxy Book5 360. It is **not** supported by any driver here, and at least one
of them lists the ID anyway.

kpagnussat's `id_table` carries both `0x0003` and `0x0007`, but nothing else in
that driver looks at which product it is talking to, so a `:0007` binds and is
then driven with a command set traced entirely off `:0003` hardware. The
observed result is an immediate stall on the first vendor control request of
the wake sequence, followed by an endless USB reset and re-init loop:

```text
[activation_wake] cmd 1/10 CTRL_OUT req=0xdb value=0x0001 index=1
Command transfer failed: endpoint stalled or request not supported
```

**This is being fixed in that driver.** Its author confirmed it in
[kpagnussat/canvasbio-cb2000#3](https://github.com/kpagnussat/canvasbio-cb2000/issues/3):
`0x0007` is gone from `id_table` in their working tree, so a `:0007` will fail
cleanly as "no driver found" and no udev rule is installed for it. That ships
with their next release, which is held until the reworked driver passes testing
on real hardware under GNOME and KDE. **Until that release is out, the
published snapshot still lists `0x0007`, so do not install it on a `:0007`.**

Reverse-engineering notes in
[myso-kr/samsung-galaxy-book-fingerprint-sensor-device-730b](https://github.com/myso-kr/samsung-galaxy-book-fingerprint-sensor-device-730b/blob/main/docs/reverse-engineering/driver-analysis.md)
describe `2df0:0007` as match-on-chip with SDCP and TLS, off a Realtek UMDF
driver, against the plain unencrypted image sensor that `:0003` is known to be.
That has since been confirmed from the vendor driver package, everything
except the TLS part. See [the vendor driver package](#the-vendor-driver-package)
below.

### What the descriptors say

A full descriptor dump from a Book5 360, posted in
[issue #17](https://github.com/jedbillyb/linux-fingerprint-drivers/issues/17),
settles what that stall means, and a copy is kept here as
[`2df0-0007-lsusb.txt`](2df0-0007-lsusb.txt) so it outlives the attachment
URL. The interface is vendor specific, class 255
subclass 2, with four endpoints:

| Endpoint | Direction | Type | Max packet |
|---|---|---|---|
| `0x01` | OUT | Bulk | 512 |
| `0x82` | IN | Bulk | 512 |
| `0x83` | IN | Interrupt | 16 |
| `0x84` | IN | Interrupt | 16 |

The `:0003` driver's author has since posted the same dump from a working
`:0003` (Galaxy Book3 360), with two control reads made against it,
[in their issue #3](https://github.com/kpagnussat/canvasbio-cb2000/issues/3#issuecomment-5623280551):

| Property | `2df0:0003` | `2df0:0007` |
|---|---|---|
| `bcdUSB` | `2.00` | `2.01` |
| `bcdDevice` | `1.27` | `f0.42` |
| Manufacturer string | `Generic` | `CanvasBio` |
| `bmAttributes` | `0xe0`, self powered, remote wakeup | `0xa0`, remote wakeup |
| Endpoints | `0x01`, `0x82`, `0x83` (16 bytes) | the same plus `0x84` (16 bytes) |
| BOS descriptor | none, `GET_DESCRIPTOR(BOS)` stalls | Microsoft OS 2.0 capability, vendor code `0x15` |
| Vendor request `0x15` | times out | returns the 432-byte WinUSB set |
| `REQ_INIT 0xDB` (first wake command) | accepted | stalls |

So these are different parts at every level that can be read without a driver.
`:0003` does have the `0x83` interrupt endpoint, but its driver never reads it
and, per its author, the Windows traces show no traffic on it. The four-endpoint
layout of `:0007` is normal for Realtek match-on-chip parts, which is where it
turned out to belong. See
[the endpoint comparison](#result-it-answers-and-enrollment-loops-at-state-3)
below.

The BOS descriptor carries a Microsoft OS 2.0 platform capability with
`CapabilityData` `00 00 03 06 b0 01 15 00`, decoding as a Windows 8.1 minimum,
a 432 byte descriptor set and vendor request code `0x15`. Fetching that set
over `bRequest=0x15` returns exactly the advertised 432 bytes, containing:

- compatible ID `WINUSB`
- `DeviceInterfaceGUID` `{62B96A71-9D46-49E7-A698-134007291217}`
- WinUSB power properties: idle enabled, 5000 ms idle timeout, system wake
  enabled

A second BOS capability of type `0x11`, payload `01 03 00 00 00`, is present
and lsusb does not decode it. Device revision is `bcdDevice f0.42`.

### What that rules in and out

**The stall is a firmware command set difference, not a broken device.** Vendor
control transfers plainly work: `bRequest=0x15` succeeds on the same control
endpoint where `bRequest=0xdb` stalls. The `:0007` firmware simply does not
implement the `:0003` command vocabulary, which is what you would expect from a
driver that was never run against it.

**`WINUSB` does not settle the match-on-chip question either way.** It means
Windows binds `winusb.sys` as the function driver and the biometric logic sits
in a user mode WBDI driver above it. A plain image sensor and a match-on-chip
sensor doing an SDCP handshake would look identical at this level, because the
handshake would be spoken by that user mode driver over the same bulk
endpoints. The
[myso-kr notes](https://github.com/myso-kr/samsung-galaxy-book-fingerprint-sensor-device-730b/blob/main/docs/reverse-engineering/driver-analysis.md)
describing `:0007` as match-on-chip with SDCP were a lead at this point. The
vendor driver package below turned them into a finding.

**The transport is ordinary, so libusb can reproduce anything Windows sends.**
The descriptor set is self-describing, so Windows binds without a vendor INF,
and nothing about the link is privileged or kernel resident. The whole protocol
therefore crosses the wire in front of any capture, and the reverse engineering
target is the user mode component that opens that interface GUID. Searching a
Samsung or CanvasBio driver package for the GUID string above is the way to
find it.

### The vendor driver package

The Windows package for `USB\VID_2DF0&PID_0007` was obtained and read, again in
[issue #17](https://github.com/jedbillyb/linux-fingerprint-drivers/issues/17).
Its INF installs a UMDF service `CanvasBioFingerprintDriver`, binary
`CanvasBioFingerprintDriver.dll`, with `CanvasBioFingerprintAdapter.dll`
registered as the WBF engine, sensor and storage adapter. The driver DLL
contains the interface GUID above verbatim, which identifies it as the user
mode component that opens the WinUSB interface.

**`2df0:0007` is match-on-chip with SDCP.** That is now a finding rather than a
lead. Strings in the driver DLL include `sdcpcli_gen_rand`, `sdcpcli_keygen`,
`sdcpcli_secret_agreement` and `sdcp enroll commit`, alongside SHA-256/384/512,
AES-128/256-GCM and AES-CCM, and on-device storage operations named
`flash_write_enrollment`, `storage_write_subtemplate` and
`flash_storage_write_verification`. So the host establishes an SDCP session and
then drives a template store that lives on the sensor. The myso-kr notes were
right on the substance. Their "TLS" is the one part to drop: the `.tls` strings
in a PE are Thread Local Storage sections, not the protocol.

**The silicon is Realtek.** The INF references `RtsMocWbdi`, which is Realtek's
own driver naming: `Rts` is their prefix, `Moc` is match-on-chip, `Wbdi` is the
Windows Biometric Driver Interface. The `2df0` vendor ID is CanvasBio's, not
Realtek's `0bda`, but that is the normal arrangement for this part family.

That last point matters more than anything else here, because **libfprint
already ships a Realtek match-on-chip driver**, contributed by Realtek Corp
themselves under LGPL-2.1-or-later, in
[`libfprint/drivers/realtek`](https://gitlab.freedesktop.org/libfprint/libfprint/-/tree/master/libfprint/drivers/realtek).
It is merged, in every distro build, and already carries Realtek MoC sensors
under three vendor IDs that are not `0bda`:

| ID | |
|---|---|
| `0bda:5813` | rts5813 |
| `0bda:5816` | rts5816 |
| `2541:fa03` | |
| `3274:9003` | Generic Realtek USB2.0 Finger Print Bridge |

A fourth under `2df0` would be unremarkable. The driver's shape fits the
descriptors: it claims interface 0, uses bulk `0x01` OUT and `0x82` IN and
ignores the interrupt endpoints, carries commands as 12-byte bulk frames, and
issues exactly one vendor **control** request in the whole driver. Its command
vocabulary also lines up with the strings above, `nor_enroll_commit` against
`sdcp enroll commit`, `co_check_duplicate` against duplicate-enrollment
reporting, plus `list`, `delete` and `clear_storage` for on-chip templates.

**So the `:0003` drivers were never the right base for `:0007`.** The open
question is no longer how to write a driver from scratch, it is whether the
upstream Realtek driver already speaks this device.

### The cheap test for that

One control transfer, the Realtek driver's `get_device_info`:

```text
bmRequestType  0xC0   vendor, device-to-host
bRequest       0x07
wValue         0x000D
wIndex         0x0000
wLength        8
```

If `:0007` returns 8 bytes there instead of stalling, it is speaking the
Realtek command set, and the next step is adding `{ .vid = 0x2df0, .pid =
0x0007 }` to that driver's `id_table` and building it. If it stalls the way
`bRequest=0xdb` does, the family is shared but the vocabulary is not, and the
bulk framing has to be traced from Windows after all.

**One caveat if it does work.** The upstream Realtek driver does not implement
SDCP, and neither does any released libfprint: issue
[#257](https://gitlab.freedesktop.org/libfprint/libfprint/-/issues/257) has
been open since 2020 and
[MR 547](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/547),
"Implement SDCP v2", is still unmerged as of v1.94.100. Recent EgisTec firmware
refuses to persist enrollments without an SDCP session, and a CB2000 whose
driver calls `sdcp enroll commit` may behave the same way, so enrollment could
appear to succeed and then not survive. That part is at least well trodden:
Microsoft publishes the protocol and an MIT-licensed reference client at
[microsoft/SecureDeviceConnectionProtocol](https://github.com/microsoft/SecureDeviceConnectionProtocol).

### Result: it answers, and enrollment loops at state 3

Run in
[issue #17](https://github.com/jedbillyb/linux-fingerprint-drivers/issues/17)
against upstream libfprint `v1.94.100-10-g6f9479c3`, with
`{ .vid = 0x2df0, .pid = 0x0007 }` added to the Realtek `id_table` and nothing
else changed. **`:0007` speaks the Realtek command set.** It answers
`get_device_info`, accepts `select_os`, reports its template count, enters
enrollment and reports `FP_FINGER_STATUS_NEEDED`. Then it never gets past
enroll state 3, which repeats rapidly with every transfer succeeding.

**State 3 is a poll, not a hang.** In the Realtek driver's enroll state machine
it is `FP_RTK_ENROLL_FINISH_CAPTURE`, which sends `co_finish_capture` (bulk
command `45 06`, 5 bytes back). `fp_finish_capture_cb` advances only when byte 0
of that reply is `00`; anything else re-enters the same state straight away,
with no delay. So a fast state 3 loop is the driver waiting for a finger
capture that the sensor never reports as done. The report also never reaches
`FP_FINGER_STATUS_PRESENT`, which is set in that same branch.

**The interrupt endpoints are probably not the difference.** libfprint's own
test recordings for the Realtek driver (`tests/realtek/device` and
`tests/realtek-5816/device`) carry the working sensors' USB descriptors:

| Endpoint | `0bda:5813` | `0bda:5816` | `2df0:0007` |
|---|---|---|---|
| `0x01` OUT bulk | 512 | 512 | 512 |
| `0x82` IN bulk | 512 | 512 | 512 |
| `0x83` IN interrupt | 16 | 64 | 16 |
| `0x84` IN interrupt | 16 | 64 | 16 |

`0bda:5813` has the same four endpoints as `:0007`, with the same sizes, and
the upstream driver ignores both interrupt endpoints there while enrollment
works. So the extra endpoints do not explain the loop on their own, though it
is not ruled out that `:0007` firmware uses them. The same recording shows a
good poll on `5813`: `45 06` answers `00 e7 d4 00 00`.

**The reply bytes: the sensor sees the finger, byte 0 never moves.** Logged
from `fp_finish_capture_cb` in issue #17:

| Contact | `finish_capture` reply |
|---|---|
| none, or light | `01 45 cf 00 00`, stable |
| firm | `01 c5 51 00 00`, reproducible |

So bytes 1 and 2 react to a firmly pressed finger and byte 0 stays `01`. That
shows finger **detection**, not a completed capture: bytes 1 and 2 could be a
live detect reading reported whether or not a capture is armed. The
recordings cannot settle it either. Every `finish_capture` reply in all three
Realtek test recordings has byte 0 `00`, with bytes 1 and 2 a per-device value
(`e7 d4` and nearby on `5813`, `e1 bc` on `5816`), and none of them catches a
working sensor in the "not yet" state.

**Capture works; the stock driver's check is right.** A diagnostic hack in #17
forced the driver past state 3 as soon as byte 2 left its baseline and logged
the 9-byte `accept_sample` (`45 08`) reply. It never returned `0c` (command
error), so there was always a real sample. It returned `03` (too left) once and
then a run of `07` (poor quality), because the hack jumped ahead on every poll
while the finger rested there, before each capture had finished. In the same
run `finish_capture` reached a genuine `00 c5 51 00 00` on its own. Byte 0 was
seen as `01`, `03` and `00`, so this firmware does report "done" the way the
upstream driver expects.

The earlier endless state 3 loop was therefore most likely contact that was too
light or too brief. **Press firmly and hold** until the stage advances.

### Result: enrollment works, single-press matching does not

With the stock Realtek driver and only the ID added, firm and held presses,
[issue #17](https://github.com/jedbillyb/linux-fingerprint-drivers/issues/17)
got this far:

- **Enrollment completes**, all 8 stages.
- **The sensor matches on the chip.** Verify reaches
  `FPI_MATCH_SUCCESS` for the enrolled finger. Its `accept_sample` reply is all
  zeros, which is also what a working `0bda:5813` returns at that point.
- **The template is stored.** Enrolling the same finger again reaches 8/8 and
  is then rejected by `co_check_duplicate` as a duplicate, which is itself an
  on-chip match against the stored templates.

Two things still fail, and between them login does not work yet:

1. **Verify fails after the match.** The Realtek driver follows a successful
   verify with `co_update_template` (bulk `05 11`, all parameters zero) and
   fails the whole action if byte 0 of the status reply is not `00`. `:0007`
   answers it with a non-zero status. Both working recordings answer
   `00 00 00 00 00`. By its name and position this is the adaptive template
   update, the one verify step that writes to the sensor's storage. fprintd runs
   verify when a single finger is enrolled.
2. **Identify reports no match with the enrolled finger**, with no protocol
   error. fprintd runs identify when two or more fingers are enrolled.

**The sensor itself says no match.** Dumps from 2026-09-19 in #17 settle where
identify fails. The template table is exactly the layout the upstream driver
reads: 10 slots of 35 bytes, slot 0 holding `01` (in use), finger byte `ff` at
offset 2 (`SUB_FINGER_01`, what the driver writes at commit) and the 28-byte
user ID from offset 3. So the driver's side of the comparison is fine. The
`IDENTIFY_FEATURE` reply starts `0b`, which is `FP_RTK_MATCH_FAIL`, the chip's
own no-match. Verify now gets the same `0b`; the one earlier successful verify
has not been reproduced.

**Leading explanation, untested: an enrollment that covers one placement.**
`co_check_duplicate` still recognises the finger, but it compares a whole new
8-sample template against the stored one, while verify compares a single
press. After each accepted enroll sample the stock driver goes straight back
to capture without waiting for the finger to lift, so a finger held down
across stages can give 8 samples of one spot. The community patch below waits
1 s for finger removal between samples and reports reliable on-chip matches.
The test asked for in #17: clear storage, re-enroll lifting and shifting the
finger between stages, then count `00` against `0b` over ten verifies.

The `05 11` status and whether an enrollment survives a reboot have since been
answered, in the next section. Still wanted: the result of that re-enroll
test, and a Windows side capture, which would show what parameters Windows
sends with `05 11`.

### Result: a community patch logs in, with a security hole

[eliasdevx/cb2000-2df0-0007-linux](https://github.com/eliasdevx/cb2000-2df0-0007-linux)
(LGPL-2.1, posted in
[issue #17](https://github.com/jedbillyb/linux-fingerprint-drivers/issues/17)
on 2026-09-18) patches the upstream Realtek driver until `:0007` works for
login. On a Galaxy Book5 360 under Kubuntu, with libfprint `1.94.100` at
`6f9479c3` and fprintd `1.94.5`, its author reports enrollment, `fprintd-verify`,
`sudo` through PAM and the KDE lock screen all working, and the enrollment
surviving a full reboot.

Two open questions from above are answered by it:

- **`co_update_template` (`05 11`) answers `01 f7 ff ff ff`**, a non-zero
  status even straight after a successful match. The patch works around it by
  ending verify at the match and never sending `05 11`.
- **A template persists across a reboot** without any SDCP session, so this
  firmware does not refuse to store enrollments the way recent EgisTec
  firmware does.

What the patch changes, read from its diff:

- adds `2df0:0007` to the `id_table`
- verify: reports a match as soon as `IDENTIFY_FEATURE` succeeds, and skips `05 11`
- enroll: 5 stages instead of 8, restarts capture after a failed sample,
  skips `co_check_duplicate`, and commits **without a user ID** (`data_len` 0)
- blocking `g_usleep` delays of 0.3 to 1 s inside the USB callbacks

**Its verify accepts any finger the chip holds a template for, not only the
enrolled print.** Stock Realtek verify reads which template the chip matched
out of the `IDENTIFY_FEATURE` reply, rebuilds it with `fp_print_from_data`, and
succeeds only if `fp_print_equal` says it is the print being verified. The
patch drops that check, and since its commit stores no user ID, nothing on the
sensor ties a template to a print any more. So, probably, though none of it is
tested yet:

- a second person enrolled on the same sensor passes verify for your account
- a finger removed with `fprintd-delete` may stay on the chip, because delete
  finds its slot by that user ID, and would then still pass
- fingers enrolled under Windows Hello on a dual-boot machine may count too

Raised in #17 on 2026-09-19. Until verify checks which template matched, treat
the patch as safe only where you are the only person whose finger has ever been
enrolled on this sensor, and keep password login enabled, as its README
already says.

It is also not in a shape to go upstream: the device checks are inline, the
sleeps block libfprint's main loop, and the unbound verify would not pass
review. A merge request needs verify bound to a template again, which is what
the identify reply and template table dumps above are for, plus a `:0007`
specific answer to `05 11`.

## Build and install

Each project ships its own instructions and they differ, so follow the one you
pick. [docs/BUILD.md](../../docs/BUILD.md) covers the shared shape: building
libfprint from source, installing over your distro's copy, PAM setup and
troubleshooting. Sensor-specific deltas:

- kpagnussat's `R2.5` needs OpenCV present at build and run time, and enrolls
  in 15 stages rather than the usual 5, so expect a longer enrollment.
- Templates are multi-frame for every driver here. Re-enroll after switching
  drivers rather than expecting old prints to carry over.
- Expect to re-touch on some verifications. A 5x4 mm capture area means two
  presses can share almost no skin, so allow three PAM attempts.

> These replace a core system library. Keep a way to reinstall your distro's
> stock libfprint, which will also silently undo the driver on the next update.

## Tested on

- Samsung Galaxy Book3 360, daily use for login and `sudo`, per
  LennartArnholdt's and kpagnussat's own reports. Both note their accuracy
  figures come from one person on one device.
- Samsung Galaxy Book2 360, reported as working but stricter, sometimes needing
  threshold tuning.
- `2df0:0003` also recorded on a Samsung 730QED by a linuxhw hardware probe
  under Fedora 38.
- `2df0:0007` on a Samsung Galaxy Book5 360: login and `sudo` with
  eliasdevx's patch, per its author, with the verify caveat
  [above](#result-a-community-patch-logs-in-with-a-security-hole). Not a
  `:0003` driver, so not in this entry's laptop list.
