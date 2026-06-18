# Contributing a device

Thanks for helping expand fingerprint sensor support on Linux. This repo
collects patches and setup notes per USB device ID so others with the same
reader can get it working.

## Submitting a new device

1. Find your USB ID with `lsusb` (the `vendor:product` pair, e.g. `27c6:55b4`).
2. Create a folder `devices/<vendor>:<product>/` using that exact lowercase ID.
3. Add the required files (below).
4. Add a row to the device table in the top-level [README.md](README.md).
5. Open a pull request, or open a
   [new-device issue](.github/ISSUE_TEMPLATE/new-device.md) if you have a fix to
   share but cannot send a PR.

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
  libfprint, what the fix does, exact build and install steps (libfprint from
  source), PAM/fprintd setup, and which distro(s) it was tested on.
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
