# Building libfprint from source (shared guide)

Almost every fix in this repo means running a patched or unreleased libfprint
instead of your distro's package. The steps are the same regardless of sensor,
so they live here and each device entry only documents what is *specific* to
that sensor.

Read the [safety notes](#safety-notes) before you start. Replacing libfprint can
lock you out of fingerprint login until you finish, and can wipe existing
enrollments.

- [1. Install build dependencies](#1-install-build-dependencies)
- [2. Get the source](#2-get-the-source)
- [3. Build](#3-build)
- [4. Install](#4-install)
- [5. Enroll and verify](#5-enroll-and-verify)
- [6. PAM setup (login / sudo / lock screen)](#6-pam-setup-login--sudo--lock-screen)
- [Keeping your distro from overwriting it](#keeping-your-distro-from-overwriting-it)
- [Troubleshooting](#troubleshooting)
- [Reverting](#reverting)
- [Safety notes](#safety-notes)

## 1. Install build dependencies

You need meson, ninja, a C toolchain, and libfprint's build dependencies (glib,
gusb, nss, pixman, cairo, gudev, gobject-introspection, and their headers).

```sh
# Debian / Ubuntu
sudo apt build-dep libfprint-2-2          # needs deb-src lines in sources.list
# or explicitly:
sudo apt install build-essential meson ninja-build pkg-config libglib2.0-dev \
  libgusb-dev libnss3-dev libpixman-1-dev libcairo2-dev libgudev-1.0-dev \
  libgirepository1.0-dev gtk-doc-tools python3-jinja2

# Fedora
sudo dnf builddep libfprint
# or: sudo dnf install meson ninja-build gcc glib2-devel libgusb-devel \
#       nss-devel pixman-devel cairo-devel libgudev-devel gobject-introspection-devel

# Arch
sudo pacman -S --needed base-devel meson ninja glib2 libgusb nss pixman cairo \
  libgudev gobject-introspection

# Void
sudo xbps-install -S base-devel meson ninja pkg-config glib-devel libgusb-devel \
  nss-devel pixman-devel cairo-devel libgudev-devel gobject-introspection
```

## 2. Get the source

**A patched fork** (most "Working" entries) - the fork URL and branch are in the
device entry's `CREDITS`:

```sh
git clone <fork-url> libfprint
cd libfprint
git checkout <branch>
```

**An unmerged upstream merge request** (every "WIP" entry) - fetch the MR branch
straight out of the libfprint GitLab, replacing `588` with the MR number from the
device entry:

```sh
git clone https://gitlab.freedesktop.org/libfprint/libfprint.git
cd libfprint
git fetch origin merge-requests/588/head:mr-588
git checkout mr-588
```

**Upstream git master** - for the entries under *Recently merged upstream*, the
driver is already in master and needs no patch:

```sh
git clone https://gitlab.freedesktop.org/libfprint/libfprint.git
cd libfprint
```

**A patch series mirrored in this repo** - if the entry has files in `patches/`,
apply them on top of the base commit named in `patches/README.md`:

```sh
git clone https://gitlab.freedesktop.org/libfprint/libfprint.git
cd libfprint
git checkout <base-commit-from-patches-README>
git am /path/to/linux-fingerprint-drivers/devices/<id>/patches/*.patch
```

If `git am` fails, `git apply --3way` the individual patch, or rebase the series
onto current master and please send the updated series back as a PR.

## 3. Build

```sh
meson setup builddir
meson compile -C builddir
```

Useful options:

- `-Ddrivers=...` limits which drivers are built (faster; check
  `meson_options.txt` for the driver name).
- `-Dintrospection=false -Ddoc=false -Dgtk-examples=false` cuts optional
  dependencies if a build dep is hard to satisfy.
- `--prefix=/usr` matches most distro packaging; the default is
  `/usr/local`, which some distros' fprintd will not load from.

Before installing, sanity-check the build with the bundled tools - no install
needed, and this is the fastest way to tell whether your sensor is recognised at
all:

```sh
sudo ./builddir/examples/list-fp-devices    # does your sensor appear?
sudo ./builddir/examples/enroll             # try an enroll against the build
```

## 4. Install

```sh
sudo meson install -C "$PWD/builddir"   # absolute path matters for sudo
sudo ldconfig
sudo pkill -9 -x fprintd                # fprintd re-spawns on demand via D-Bus
fprintd-list "$USER"                    # should now name your sensor
```

If `fprintd-list` still reports no devices, see
[Troubleshooting](#troubleshooting).

## 5. Enroll and verify

```sh
fprintd-enroll "$USER"    # press repeatedly; vary angle, edge, and pressure
fprintd-verify "$USER"    # want: verify-match
```

`fprintd-enroll -f <finger>` enrolls a specific finger (`right-index-finger`,
`left-thumb`, ...). Enroll the same finger with deliberately varied positions -
most "verify is unreliable" reports are actually under-varied enrollments.

Enrollments live in `/var/lib/fprint/<user>/`. Deleting that directory (or
`fprintd-delete "$USER"`) resets a user's prints, which is worth doing after
swapping drivers so stale templates are not matched against.

## 6. PAM setup (login / sudo / lock screen)

Prefer your distro's helper where one exists:

```sh
# Debian / Ubuntu
sudo pam-auth-update --enable fprintd

# Fedora / RHEL
sudo authselect enable-feature with-fingerprint
sudo authselect apply-changes
```

On distros without a helper (Arch, Void, Gentoo, ...), add fprintd to the PAM
stack your services chain to - `/etc/pam.d/system-auth` on Arch and Void.
**Back the file up first**, then add above the `pam_unix.so` auth line:

```
auth sufficient pam_fprintd.so
```

`sufficient` means a successful scan authenticates and your password still works
as a fallback. Never use `required` - a broken sensor then locks you out
entirely. Keep a root shell open while you test, and test `sudo -k; sudo true`
before you log out.

Some greeters and lockers need their own PAM file touched
(`/etc/pam.d/gdm-fingerprint`, `/etc/pam.d/swaylock`, ...) and GNOME/KDE both
have separate "fingerprint login" toggles in Settings.

## Keeping your distro from overwriting it

A packaged libfprint update will silently replace your patched library and
fingerprint auth will stop working. Hold the package:

```sh
# Debian / Ubuntu
sudo apt-mark hold libfprint-2-2

# Fedora
sudo dnf versionlock add libfprint          # needs dnf-plugin-versionlock

# Arch - add to /etc/pacman.conf
IgnorePkg = libfprint

# Void - add to /etc/xbps.d/10-ignore.conf
ignorepkg=libfprint
```

Packaging the patched build instead (a local `PKGBUILD`, `xbps-src` template, or
`checkinstall`) is tidier if you plan to keep the machine long-term.

## Troubleshooting

**Debug logging.** Almost every report needs this:

```sh
sudo pkill -9 -x fprintd
sudo G_MESSAGES_DEBUG=all FP_DEBUG=all /usr/libexec/fprintd -t   # path varies
# then, in another terminal:
fprintd-enroll "$USER"
```

`fprintd` lives at `/usr/libexec/fprintd`, `/usr/lib/fprintd`, or
`/usr/lib/fprintd/fprintd` depending on distro.

**No devices found.**

- Confirm the sensor is on USB at all: `lsusb`, and `tools/detect.sh` in this
  repo to match it against known entries.
- Check the driver was actually built: `sudo ./builddir/examples/list-fp-devices`.
- Check libfprint's udev rules were installed and reloaded -
  `/usr/lib/udev/rules.d/60-fprint-autosuspend.rules` plus any driver-specific
  rules; then `sudo udevadm control --reload && sudo udevadm trigger`.
- Check nothing is loading the *old* library:
  `ldd /usr/libexec/fprintd | grep fprint` and `ls -l /usr/lib/libfprint-2.so*`.
  A `--prefix=/usr/local` install next to a distro `/usr` install is the usual
  cause.

**Device claimed / busy.** Something else already holds it - another `fprintd`,
a leftover example binary, or a vendor daemon. `sudo pkill -9 -x fprintd` and
retry.

**Works as root, not as your user.** A permissions problem: your user needs to
reach fprintd over D-Bus (fprintd's polkit rules cover this), not the USB device
directly. Check `journalctl -u polkit` and that you are in an active session
(`loginctl session-status`).

**Enroll succeeds, verify fails.** Re-enroll with more, more varied captures,
and delete old templates first (`fprintd-delete "$USER"`). If your entry
mentions matcher thresholds, that is the knob.

**Suspend/resume breaks the sensor.** Common on Goodix and ELAN parts. Try
disabling USB autosuspend for the device via a udev rule, and check the device
still appears in `lsusb` after resume.

## Reverting

Reinstall the distro package to get back to a known state:

```sh
# Debian/Ubuntu
sudo apt-mark unhold libfprint-2-2 && sudo apt install --reinstall libfprint-2-2
# Fedora
sudo dnf reinstall libfprint
# Arch
sudo pacman -S libfprint
# Void
sudo xbps-install -f libfprint
sudo ldconfig && sudo pkill -9 -x fprintd
```

Then disable fingerprint PAM (`sudo pam-auth-update --disable fprintd`,
`sudo authselect disable-feature with-fingerprint`, or remove the
`pam_fprintd.so` line you added).

`sudo ninja -C builddir uninstall` also works if you still have the build
directory, but reinstalling the package is more reliable because it restores
files the uninstall step may leave behind.

## Safety notes

- **Never make fingerprint auth `required`.** Password fallback keeps you out of
  a lockout.
- **Keep a second, already-authenticated root shell open** while editing PAM.
- **Back up `/etc/pam.d/` files before editing them.**
- Installing over the system libfprint may wipe `/var/lib/fprint/` enrollments.
- Fingerprint auth is a convenience, not a strong security boundary - a sensor
  driven by reverse-engineered, unaudited code even less so. Judge accordingly
  on a machine that matters.
