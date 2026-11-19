# Patches for ELAN ARM-M4 (0c77)

`0001-elanmoc2-driver-with-04f3-0c77.patch` applies to upstream libfprint at
commit `6f9479c3d55f847c1b3769f28ceb99227f9858cf` (v1.94.100 + 10):

```sh
git clone https://gitlab.freedesktop.org/libfprint/libfprint.git
cd libfprint
git checkout 6f9479c3d55f847c1b3769f28ceb99227f9858cf
patch -Np1 -i 0001-elanmoc2-driver-with-04f3-0c77.patch
```

It adds the whole `elanmoc2` driver, so it does not need Davide Depau's fork as
a base. The driver also carries the IDs of the original branch (`0c00`, `0c4c`,
`0c5e`, `0c7c`, `0c90`); those were not tested with this patch.

Source: https://github.com/inumineq/libfprint-elan-0c77

That repository also has an experimental second patch that waits for the
sensor to report ready after opening it. It is meant to address the known
limitation in the entry README and has not been tested in that situation, so
it is not included here.
