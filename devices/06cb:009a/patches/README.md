# Patches for Synaptics Prometheus (06cb:009a)

Route 1 (python-validity) has no patch series: it is a standalone userspace
daemon, not a libfprint patch. Install the packages linked in `../CREDITS`
(Ubuntu PPA, Arch AUR, Fedora COPR) together with open-fprintd.

Route 2 (native libfprint-2-tod1 driver) is a separate driver, not a libfprint
patch series either - it is a `libfprint-2-tod1` module loaded by a TOD-enabled
libfprint (AUR `libfprint-tod-git`). Its Arch packaging patch
(`0001-arch-fixes-clean-slate-init-and-fwext-uploader.patch`) applies to the
driver, not to libfprint:

  driver base: blackandcold/t480s-fingerprint-driver-for-linux
               branch arch-adoption, commit 216361ebeccb3d427844a4f15be8d6f96eaaf1c3
  patch + PKGBUILD: https://github.com/hustles/libfprint-2-tod1-synaptics009a

Nothing is mirrored into this directory; this file points at the sources so the
provenance is traceable.
