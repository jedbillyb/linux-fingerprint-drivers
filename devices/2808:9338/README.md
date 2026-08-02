# FocalTech FT9201

**Status: WIP (unmerged upstream MR)**

Device ID(s): `2808:9338, 2808:93a9`

This is a driver that has been submitted to the **official libfprint project**
but is **not merged yet**, so it is not in any released libfprint. Tracked here so
people with this sensor can find and build the work in progress.

## Upstream merge request

- libfprint MR !572: https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/572
- Author: 0xCoDSnet (@0xCoDSnet)


## What it does

New driver for the FocalTech FT9201 sensor.

## Hardware notes (measured, `2808:93a9`)

Reported in [issue #2](https://github.com/jedbillyb/linux-fingerprint-drivers/issues/2)
from a live device, and worth recording because a couple of write-ups assume
otherwise:

- USB interface class **255** (vendor-specific), `bcdDevice 1.00`.
- **Exactly two bulk endpoints and no interrupt endpoint**: `0x02` OUT (16 B),
  `0x83` IN (32 B). Several existing descriptions assume an interrupt endpoint
  on `93a9`; there is none on this revision.
- Image is 64x80, 8 bpp, read as exactly `width * height` bytes.
- Vendor request **`0x6F`** (length in `wValue`, address in `wIndex`) is what
  arms a bulk read here. Open drivers that use `0x35` arm nothing on this
  revision - a plausible explanation for the long-standing "initialises but
  never reads" reports against this sensor.

Some modules also expose `2808:6553` alongside `93a9`. That second function is
the FT9365 secure-storage companion and cannot capture, even though
`focaltech_moc` binds it and it answers the protocol - see the
[caveat in `devices/2808:6553`](../2808:6553/README.md#caveat-on-dual-function-ft9201-modules).

## How to use it

The code lives in the merge request, not in this repo. To try it, check out the
MR's source branch of libfprint and build from source (see
[docs/BUILD.md](../../docs/BUILD.md) for the shared build, install, PAM and
troubleshooting steps), or follow any instructions in the MR discussion.

```sh
# fetch the MR branch into a libfprint checkout, e.g.
git fetch https://gitlab.freedesktop.org/libfprint/libfprint.git \
  merge-requests/572/head:mr-572
git checkout mr-572
```

## Tested on

Not documented.

## License

Part of libfprint (LGPL-2.1).

## Alternative route: vendor matching engine on Linux

[OMGrant/ft9201-libfprint](https://github.com/OMGrant/ft9201-libfprint)
(LGPL-2.1, 20+ stars, active) is a working driver for `2808:93a9` that takes a
different approach: the libfprint driver is open, but instead of NBIS it calls
**FocalTech's own Windows matching engine** (`ftWbioEngineAdapter.dll`) through a
small in-process PE loader. No Wine, and it runs under fprintd's
`MemoryDenyWriteExecute` hardening.

Trade-offs: you must supply the vendor DLL yourself, matching happens inside a
blob nobody can fix, and it is x86-64 only. Tested by that author on the FT9348W
variant of `2808:93a9`.

Its [`PORTING.md`](https://github.com/OMGrant/ft9201-libfprint/blob/HEAD/PORTING.md)
generalises the method to other Windows-Hello-only readers, including SDCP
sensors, which makes it worth reading for anyone attacking a sensor in the
[gap-map](../../docs/unsupported-devices.md).

## Alternative route: clean-room protocol spec (captures, does not match)

[NBN-PATRIC/ft9201-libfprint](https://github.com/NBN-PATRIC/ft9201-libfprint)
(LGPL-2.1, clean-room, no blobs) documents the `2808:93a9` protocol and ships a
WIP driver built on it. **It captures but does not authenticate** - the author
is explicit about this, and so is the driver header.

What works: acquisition against libfprint master (1.94.100), `fprintd`
recognises the device, frames are captured, ridge structure resolves at an
8-14 px period, and enrollment completes.

What does not: verification never matches, and the author's follow-up
measurements argue this is **not** a tuning problem. NBIS minutiae extraction
yields under 3 minutiae per frame against a Bozorth threshold of 40;
multi-frame mosaicking raises the count with seam artifacts that score 0
between two composites of the same finger; and NCC over subtemplates separates
genuine from impostor by d' = 0.06 in natural use. Fixed-pattern-noise removal,
a wider rotation search, Gabor ridge enhancement and larger scoring windows
were all measured and none closed the gap. The stated root cause is window
size: at 3.2 x 4.1 mm, eleven natural touches spanned essentially the full
rotation range, so a physically rotated finger presents a *different patch of
skin* rather than a rotated copy of the same one - synthetic rotation of one
sample is recovered at 0.98, so the rotation search itself is fine.

The sensor is not the limitation - the vendor library authenticates on this
same hardware - so closing the gap means reproducing a proprietary feature
extractor. Treat the repo as a protocol reference and capture path, not as a
working login. See its `MATCHING.md` for the full account and `tuning/` for the
harnesses.
