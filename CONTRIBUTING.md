# Contributing a device

Thanks for helping expand fingerprint sensor support on Linux. This repo
collects patches and setup notes per USB device ID so others with the same
reader can get it working.

## Submitting a new device

1. Find your USB ID with `./tools/detect.sh` or `lsusb` (the `vendor:product`
   pair, e.g. `27c6:55b4`), and check it does not already have an entry.
2. Create a folder `devices/<vendor>:<product>/` using that exact lowercase ID.
   Sensors that are not on USB (SPI, I2C, cros_ec) use a short descriptive name
   instead, e.g. `devices/mafp8800/`.
3. Add the required files (below).
4. Add a row to the right table in the top-level [README.md](README.md):
   *Working fixes*, *In progress*, *Recently merged upstream*, or *Experimental
   community forks*.
5. Run `python3 tools/check-repo.py` and fix anything it reports.
6. Open a pull request, or open a
   [new-device issue](https://github.com/jedbillyb/linux-fingerprint-drivers/issues/new?template=new-device.yml)
   if you have a fix to share but cannot send a PR.

You do not need a driver to contribute. A **device report** confirming an entry
works (or has broken) on your distro, or a protocol dump for something in the
[gap-map](docs/unsupported-devices.md), is genuinely useful on its own.

## Folder structure

```
devices/<vendor>:<product>/
  README.md      # required - sensor info + build/install/setup instructions
  CREDITS        # required - author(s) and links to upstream fork/branch
  patches/       # patch files (.patch / .diff) against a stated libfprint base
    .gitkeep
```

## Required files

- **README.md** - must cover: the chip/sensor name, what is broken in upstream
  libfprint, what the fix does, anything sensor-specific about building or
  installing it, and which distro(s) it was tested on (with a `## Tested on`
  section). Do **not** repeat the generic build/install/PAM steps: link
  [docs/BUILD.md](docs/BUILD.md) and only describe the deltas, so a fix to the
  shared instructions benefits every entry.
- **CREDITS** - the author handle(s) and a link to the source branch/fork the
  patches come from, so changes can be traced and credited.
- **patches/** - the actual `.patch`/`.diff` files, or a clear pointer to the
  branch they live on. State the libfprint version/commit they apply against.

## Attribution

libfprint driver work is built on the efforts of many people. If your fix is
based on someone else's branch or reverse-engineering, **credit them in
CREDITS** and link the original source. Do not strip existing copyright headers
from patched files.

## License compatibility

libfprint is **LGPL-2.1**. Any code or patches you contribute here must be
LGPL-2.1-compatible. By submitting, you agree your contribution is licensed
under LGPL-2.1. Do not include code under incompatible licenses.
