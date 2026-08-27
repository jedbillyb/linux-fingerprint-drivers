# Patches

This sensor is served by an out-of-tree **TOD** driver — a shared module that
libfprint loads at runtime — not by a patch series against libfprint's own
source tree. There are therefore no `.patch` files here; the code lives in its
own repository and is built and installed as a module.

- Source: https://github.com/Sigfrodr/libfprint-goodixtls
- Base commit: d7ed1db0c7a229c986a3879e91677f701388a8c1 (branch `main`)
- Builds against: libfprint-2-tod1 1.94.7+tod1 (Ubuntu 24.04), i.e. the
  `libfprint-2-tod-1` pkg-config module; the driver targets the TOD ABI, not a
  specific upstream libfprint commit.

Build and install are automated by `sudo ./install.sh` in that repository.
