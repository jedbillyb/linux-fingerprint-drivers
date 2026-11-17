# FPC Match-on-Host / fpcmoh (USB 10a5:9800)

**Status: Working via the out-of-tree fpcmoh packaging.**

Fingerprint Cards (FPC) sensor.

## Hardware

Seen on ThinkPad E14 Gen5, ThinkPad E15 Gen 4 and ThinkBook 14 G4 IAP. The
sensor reports a 112x88 image; firmware 27.26.23.30 (E14 Gen5), 27.26.23.18
(ThinkBook 14 G4 IAP) and 16.26.23.22 (E15 Gen 4, as shipped) have been seen.

## Sensor firmware

Units on 16.x firmware exist (`lsusb` shows `L:0001 FW:16.26.23.xx`). What that
means depends on the route:

- **Lenovo's package** (`r1slm01w`/`r1slm02w`) and the fpcmoh builds derived
  from it require firmware **27.26.23.19 or newer**, per Lenovo's readme.
- **The Ubuntu TOD module** has been reported working on 16.26.23.22 and
  16.26.23.14 (E14 Gen 4,
  [LP: #2024145](https://bugs.launchpad.net/bugs/2024145) comments #2 and #3).

Getting the update through fwupd is currently awkward:

- Stable LVFS only carries `com.fingerprints.lenfy.firmware` 27.26.23.19, which
  has no CHID requirement. fwupd 2.x refuses it for this device ("generic GUID
  requires a CHID, child, parent or sibling requirement"), so it is never
  offered. This is intentional, see
  [fwupd#5573](https://github.com/fwupd/fwupd/issues/5573).
- `com.fingerprints.Lenovo.cs23.9800.firmware` 27.26.23.50 *is* restricted to
  specific models (its CHIDs include ThinkPad E15 Gen 4), but it has only been
  on the `lvfs-testing` remote since 2024. Promotion to stable is requested in
  [fwupd/firmware-lenovo#653](https://github.com/fwupd/firmware-lenovo/issues/653).
  Check with `fwupdmgr enable-remote lvfs-testing && fwupdmgr refresh &&
  fwupdmgr get-updates`, and disable the remote again afterwards.

Lenovo's readme also tells you to build fwupd from source and `ninja install`
it. That leaves a `libfwupd.so.3` in `/usr/local/lib/x86_64-linux-gnu` that
later shadows the distro library and breaks the packaged `fwupd.service`
(`version 'LIBFWUPD_2.0.x' not found`). If you did that in the past, move the
`/usr/local` fwupd files aside and run `sudo ldconfig`.

## What was broken

Upstream libfprint does not support this FPC sensor, so it is unrecognised.

## What the fix does

Adds the `fpcmoh` (FPC match-on-host) driver to libfprint plus the udev rules
needed for the device, enabling enroll and verify.

The upstream attempt to land this driver, libfprint MR
[!396](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/396)
("fpcmoh: Support FPC moh (match on host) devices", PID 0x9800), was **closed
without merging**, so the out-of-tree packaging below remains the working route.

The driver links against `libfpcbep.so`, a proprietary library from FPC that
Lenovo ships in
[r1slm01w.zip](https://download.lenovo.com/pccbbs/mobiles/r1slm01w.zip)
(sha256 `c7290f2a70d48f7bdd09bee985534d3511ec00d091887b07f81cf1e08f74c145`).
It is not mirrored here.

## Build and install

The cleanest source is xuwd1's AUR package `libfprint-fpcmoh-git` (see
`CREDITS`). Arch:

```sh
# AUR helper, e.g.
yay -S libfprint-fpcmoh-git
sudo pkill -9 -x fprintd
fprintd-list "$USER"
sudo fprintd-enroll "$USER"
```

On other distros, build libfprint with the fpcmoh driver from that source and
install the accompanying udev rules. furcom's repo (archived, read-only) packaged
this for Fedora/dnf.

### Ubuntu (TOD module)

On Ubuntu there is no need to build anything. FPC's driver is packaged as a
libfprint TOD module, `libfprint-2-tod1-fpc`, in
[`ppa:libfprint-tod1-group/ppa`](https://launchpad.net/~libfprint-tod1-group/+archive/ubuntu/ppa).
It loads into Ubuntu's stock `libfprint-2-tod1`, so nothing is rebuilt or
replaced:

```sh
sudo add-apt-repository ppa:libfprint-tod1-group/ppa
sudo apt update
sudo apt install libfprint-2-tod1-fpc
sudo pam-auth-update --enable fprintd
fprintd-enroll && fprintd-verify
```

The PPA has builds for focal (20.04), jammy (22.04) and noble (24.04). There
is **no build for 26.04 yet**. Inclusion in the Ubuntu archive for 26.04 and
later is requested in
[LP: #2024145](https://bugs.launchpad.net/bugs/2024145); if you are affected,
mark it "affects me" there.

### Debian / Ubuntu (patch against libfprint v1.94.10)

[`patches/0001-fpcmoh-support-10a5-9800-v1.94.10.patch`](patches/) is MR !396
rebased onto libfprint **v1.94.10**, the version Debian forky ships. Follow
[docs/BUILD.md](../../docs/BUILD.md) with these deltas:

1. Get the blob and give it a soname. Without one, the linker records the
   blob's absolute build-time path in `libfprint-2.so`:

   ```sh
   wget https://download.lenovo.com/pccbbs/mobiles/r1slm01w.zip
   unzip r1slm01w.zip
   mkdir -p ~/fpcbep
   cp FPC_driver_linux_27.26.23.39/install_fpc/libfpcbep.so ~/fpcbep/
   patchelf --set-soname libfpcbep.so ~/fpcbep/libfpcbep.so
   ```

2. Check out `v1.94.10`, apply the patch, and point meson at the blob with the
   `fpcbep_dir` option the patch adds:

   ```sh
   git checkout v1.94.10
   git apply /path/to/0001-fpcmoh-support-10a5-9800-v1.94.10.patch
   meson setup builddir --prefix=/usr/local --libdir=lib/x86_64-linux-gnu \
       -Dfpcbep_dir="$HOME/fpcbep" -Dudev_hwdb=disabled -Dudev_rules=disabled \
       -Ddoc=false -Dgtk-examples=false -Dintrospection=false -Dinstalled-tests=false
   meson compile -C builddir
   ```

3. Install the library, the blob and Lenovo's udev rule:

   ```sh
   sudo meson install -C "$PWD/builddir"
   sudo install -m 0644 ~/fpcbep/libfpcbep.so /usr/local/lib/x86_64-linux-gnu/
   sudo install -m 0644 FPC_driver_linux_libfprint/install_libfprint/lib/udev/rules.d/60-libfprint-2-device-fpc.rules /etc/udev/rules.d/
   sudo ldconfig
   ```

On Debian multiarch, `/usr/local/lib/x86_64-linux-gnu` comes before
`/usr/lib/x86_64-linux-gnu` in `/etc/ld.so.conf.d/x86_64-linux-gnu.conf`. The
packaged `fprintd` therefore loads this build while `libfprint-2-2` stays
installed, and a later `apt upgrade` does not overwrite it. To revert, delete
the installed files and run `sudo ldconfig`. Check which library is picked up
with `ldconfig -p | grep libfprint-2.so.2`.

`fprintd-enroll` asks for your password through polkit (`auth_self_keep`). On
desktops without a visible polkit agent (for example a bare Hyprland or sway
session), the prompt can time out and enrolling then fails with
`EnrollStart failed: Timeout was reached`. Running a polkit agent, or
`sudo fprintd-enroll "$USER"`, avoids this.

## PAM setup

Enable fprintd in your PAM stack: distro helper where there is one, otherwise
`auth sufficient pam_fprintd.so`. Never `required`. Full steps per distro are in
[docs/BUILD.md](../../docs/BUILD.md#6-pam-setup-login--sudo--lock-screen).

## Tested on

- ThinkPad E14 Gen5: Fedora (furcom's packaging); Arch via the AUR package.
- ThinkPad E14 Gen 5 (21JKS1Q500), sensor firmware 27.26.23.30: Debian forky
  with the v1.94.10 patch above and Debian's fprintd 1.94.5. Enroll,
  verify-match with the enrolled finger and verify-no-match with another finger.
- ThinkBook 14 G4 IAP (21DH), sensor firmware 27.26.23.18: Ubuntu 24.04 with
  the TOD module above (`libfprint-2-tod1` 1:1.94.7+tod1-0ubuntu5~24.04.8,
  `libfprint-2-tod1-fpc` 27.23.44.2+2404-0ubuntu1, fprintd 1.94.3). Enroll,
  verify, GDM login, sudo and lock screen.
- ThinkPad E15 Gen 4 (21E6), sensor firmware 16.26.23.22 updated to
  27.26.23.19: Ubuntu 24.04, fprintd 1.94.3, with FPC's own fpcmoh source
  ([fingerprint-cards/libfprint@ad19338](https://github.com/fingerprint-cards/libfprint/commit/ad1933814a775c11f9581507910bae525c67ff2a),
  which `dlopen()`s `libfpcbep.so` at runtime) rebuilt into Ubuntu's
  `libfprint` 1:1.94.7+tod1 source package. Enroll, verify, GDM login and sudo.
  The TOD module above is the simpler route on Ubuntu.
