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

Its [`PORTING.md`](https://github.com/OMGrant/ft9201-libfprint/blob/main/PORTING.md)
generalises the method to other Windows-Hello-only readers, including SDCP
sensors, which makes it worth reading for anyone attacking a sensor in the
[gap-map](../../docs/unsupported-devices.md).
