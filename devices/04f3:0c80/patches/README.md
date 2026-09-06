# Patches for ELAN ARM-M4 (0c80)

`0001-elanmoc2-add-04f3-0c80.patch` applies to Davide Depau's libfprint fork at
commit `11f0316d069cc90c154c8cb0e46478388c5e2a74` ("WIP add 0c7c"):

```sh
git clone https://gitlab.freedesktop.org/Depau/libfprint.git
cd libfprint
git checkout 11f0316d069cc90c154c8cb0e46478388c5e2a74
git apply 0001-elanmoc2-add-04f3-0c80.patch
```

It does **not** apply to the current `xerootg` branch; the quirk names and the
surrounding code differ there. Rebasing it onto a maintained branch, and
solving the erase timeout documented in the entry README, are the two open
pieces of work.

Source: https://gist.github.com/ChuChua-Tech/37e7636c0276974547ff36e3ee51030e
