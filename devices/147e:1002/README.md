# UPEK Touchstrip (upeksonly)

**Status: WIP (unmerged upstream MR, Draft)**

Device ID(s): `147e:1002`

This is a driver that has been submitted to the **official libfprint project**
but is **not merged yet**, so it is not in any released libfprint. Tracked here so
people with this sensor can find and build the work in progress.

## Upstream merge request

- libfprint MR !585: https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/585
- Author: Nikolay Metchev (@nikolaymetchev)
- Marked **Draft** by the author.

## What it does

Experimental support added to the existing upeksonly driver.

## How to use it

The code lives in the merge request, not in this repo. To try it, check out the
MR's source branch of libfprint and build from source (see
[docs/BUILD.md](../../docs/BUILD.md) for the shared build, install, PAM and
troubleshooting steps), or follow any instructions in the MR discussion.

```sh
# fetch the MR branch into a libfprint checkout, e.g.
git fetch https://gitlab.freedesktop.org/libfprint/libfprint.git \
  merge-requests/585/head:mr-585
git checkout mr-585
```

## Tested on

Not documented.

## License

Part of libfprint (LGPL-2.1).

## Related: image quality fixes for UPEK swipe sensors

libfprint MR [!576](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/576) ("upeksonly: Add image enhancement function for
upek-sensors", Pascal Hoehnel / @phoehnel) targets the underlying reason these
sensors match poorly: at 144x384 a perfect scan yields at most ~18 minutiae,
under the threshold of 20. It adds contrast stretching plus 2x upscaling for
`upektc_img`, lowers the rev1 `bz3_threshold` to 20, drops `FPI_IMAGE_PARTIAL`
(which discarded a significant slice of a 144px-wide image), and raises enroll
stages to 10.

Worth combining with this entry's work if you have any UPEK swipe reader, including
already-"supported" ones.
