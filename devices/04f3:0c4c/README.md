# ELAN Match-on-Chip / elanmoc2 (USB 04f3:0c4c, 04f3:0c00)

ELAN match-on-chip fingerprint reader. The same driver also covers `04f3:0c00`.

## What was broken

Upstream libfprint has no driver that handles these ELAN match-on-chip readers,
so they are unrecognised and `fprintd-enroll` cannot use them.

## What the fix does

Adds the **elanmoc2** driver to libfprint, which speaks the match-on-chip
protocol for these readers (enroll, verify, identify, and template management
are handled on the sensor). Once the elanmoc2 driver lands upstream this entry
becomes obsolete.

## Build and install

The driver lives on the **`elanmoc2`** branch of Depau's libfprint fork on
freedesktop GitLab (see `CREDITS` for the link). Build it like any libfprint:

```sh
git clone <elanmoc2 fork>      # see CREDITS
cd libfprint
git checkout elanmoc2
meson setup builddir --prefix=/usr
meson compile -C builddir
sudo meson install -C "$PWD/builddir"
sudo ldconfig
```

Debian/Ubuntu users can instead use Greek64's `.deb` packaging of the same
driver (see `CREDITS`).

After install, restart fprintd and confirm the device is listed:

```sh
sudo pkill -9 -x fprintd
fprintd-list "$USER"
sudo fprintd-enroll "$USER"
```

## PAM setup

Enable fprintd in your PAM stack (e.g. `pam-auth-update --enable fprintd` on
Debian/Ubuntu, or add `auth sufficient pam_fprintd.so` to the relevant
`/etc/pam.d` file). Password fallback stays available.

## Tested on

- Debian / Ubuntu (via the elanmoc2 `.deb` packaging). The driver branch builds
  on other distros from source.
