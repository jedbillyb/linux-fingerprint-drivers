# Goodix GF5288 / GM168SEC (USB 27c6:550c)

**Status: Working via community libfprint drivers, not upstream yet. Enroll, verify, `sudo` and the KDE lock screen work on the Lenovo Yoga 9 14IAP7.**

Goodix TLS ("SEC") match-on-host press sensor, firmware `GF5288_GM168SEC_APP_13021`
on the Yoga 9 14IAP7. Same GF5288 + GM168SEC family as `27c6:533c`, driven by the
`goodix53x5` driver family from AndyHazz/goodix53x5-libfprint.

## What was broken

Upstream libfprint has no driver for it, so fprintd reports `No devices available`.
The Lenovo 550a TOD blob does not work either (`USB error on device 27c6:550c:
Invalid parameter [-2]`).

Like the other TLS Goodix readers, each sensor has its own 32-byte pre-shared key
(PSK), created and sealed by the Windows driver when the sensor was first paired.
Firmware 13021 also never sends the asynchronous finger-down event the
`goodix53x5` driver expects, so contact has to be detected by polling.

## The drivers

There are two routes. **They are mutually exclusive**: a sensor reflashed by route B
is refused by route A.

| Route | Source | Sensor writes | Needs |
|---|---|---|---|
| A. Keep stock firmware | [the-great-king-bart/goodix-550c-linux-driver](https://github.com/the-great-king-bart/goodix-550c-linux-driver), Debian 13 packages at [fdjfnd222dd/goodix-550c-linux-debian](https://github.com/fdjfnd222dd/goodix-550c-linux-debian) | None (persistent commands denied in the driver) | The original Windows install, to recover the PSK once |
| B. Reflash to 13022 | [brianporeilly/goodix-550c-driver](https://github.com/brianporeilly/goodix-550c-driver) | Reflashes firmware 13022 (from the Yoga 9 14IRP8 Windows driver) and resets the PSK | No Windows install |

### Route A: what the fix does

A fail-closed patch series on top of brianporeilly's driver and libfprint v1.94.10:

- accepts only firmware `GF5288_GM168SEC_APP_13021` and refuses anything else,
- denies every persistent sensor command (no reflash, no PSK write),
- reads the PSK from a root-only file and wipes it from memory after the TLS handshake,
- polls raw capacitance deltas for finger-down, since this firmware never sends the event,
- refuses blank or finger-covered reference frames (the sensor returns blank frames for
  about 11 s after sleep, which otherwise poisons enrolled templates),
- matches with SIGFM at a fixed threshold of 150.

Measured on one Yoga 9 14IAP7: 85% genuine first-try match, 0 impostor accepts
(max impostor score 3 against threshold 150), 0 failed sensor opens in 100+ opens.

## Install

- **Debian 13 (trixie):** packages and a step-by-step guide (PSK recovery, install,
  enroll, PAM) at [fdjfnd222dd/goodix-550c-linux-debian](https://github.com/fdjfnd222dd/goodix-550c-linux-debian/blob/main/docs/DEBIAN-INSTALL.md).
  It replaces `libfprint-2-2` with a patched build (held against upgrades) and ships an
  opt-in PAM profile where the password always keeps working.
- **Ubuntu 26.04:** the original project builds an external TOD module for Ubuntu's
  `libfprint 1.95.1+tod1`, see its README.
- **Route B:** follow brianporeilly/goodix-550c-driver's README.

Generic build and PAM steps: [docs/BUILD.md](../../docs/BUILD.md).

## Tested on

- Route A: Debian 13 (trixie), kernel 6.12, KDE Plasma, fprintd 1.94.5, Lenovo Yoga 9
  14IAP7 (82LU): enroll, `fprintd-verify`, `sudo` and the KDE lock screen.
  Also Ubuntu 26.04 via the TOD module (original project).
- Route B: reported working on the Yoga 9 14IAP7 (including Debian) and the Yoga 9 14IRP8,
  see [goodix-fp-dump #59](https://github.com/goodix-fp-linux-dev/goodix-fp-dump/issues/59) and the project's README.

## Caveats

- Both routes are unofficial, reverse-engineered and unaudited.
- Route A needs the Windows install that paired the sensor. If Windows was wiped, the
  PSK is gone and only route B can help.
- Route B's reflash is one way.
- Stored templates are not encrypted (a libfprint property).
