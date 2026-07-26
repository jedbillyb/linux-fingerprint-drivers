# EgisTec EgisTec0570 - calibration fix (USB 1c7a:0570, 1c7a:0571)

**Status: Claimed upstream by the `egis0570` driver, but unreliable. Fix MR open.**

The in-tree `egis0570` driver covers `1c7a:0570` and `1c7a:0571`, but calibration
is not implemented properly, which shows up as erratic captures and unreliable
verification (libfprint
[issue #418](https://gitlab.freedesktop.org/libfprint/libfprint/-/issues/418)).

## What the fix does

libfprint MR [!548](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/548)
("fix: calibration for egis0570", Saeed/Ali Rk / @saeedark) implements sensor
calibration. The author reports the calibration part works as intended -
"not perfect but reasonable".

The MR also wants to store calibration data persistently, which needs
libfprint's `benzea/persistent-data` work plus the matching fprintd branch
(see MR [!368](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/368)).
Without those, calibration is redone rather than saved, which is fine
functionally.

## How to try it

```sh
git clone https://gitlab.freedesktop.org/libfprint/libfprint.git
cd libfprint
git fetch origin merge-requests/548/head:mr-548
git checkout mr-548
```

Then build per [docs/BUILD.md](../../docs/BUILD.md).

## Tested on

- The MR author's own hardware; calibration confirmed, persistence not.
- Reports from other `1c7a:0570`/`0571` owners welcome.

## License

Part of libfprint (LGPL-2.1).
