# Find your laptop

Fingerprint reader support on Linux, indexed by **laptop model** rather
than by USB ID. If `fprintd-enroll` fails on your machine, find it below.

This page is generated from the device entries and the
[gap-map](unsupported-devices.md); it lists every model those name, and
nothing else. Absence from this page is not evidence that a reader works
or does not: it usually just means nobody has reported that model yet.
Many sensors also ship in machines nobody has written down here, so if
your exact model is missing, **match on the USB ID instead**:

```sh
lsusb        # find the reader, e.g. 27c6:55b4
```

then look it up in the [main README](../README.md), or run
`./tools/detect.sh` to have it matched for you.

30 model listings map to a catalogued sensor; the rest are on the
gap-map with no known fix, and a protocol dump for any of them is welcome.

**Adding your machine** is the single most useful small contribution here.
Open a [device report](https://github.com/jedbillyb/linux-fingerprint-drivers/issues/new?template=device-report.yml)
with your model and `lsusb` line, or add a line to the sensor's
`devices/<id>/MODELS` file and open a PR.

Status legend: **Working** (enroll and verify reliable), **Working (vendor
blob)** (only via a proprietary driver, see the entry's caveats),
**Partial**, **Merged upstream** (in libfprint git, build from source),
**WIP** (unmerged work exists), **Unreliable** (claimed upstream but fails
in practice), **Stale** (abandoned lead), **No known fix**.

## Lenovo

| Laptop model | USB ID | Sensor | Status | Where to go |
|--------------|--------|--------|--------|-------------|
| Lenovo IdeaPad Flex 5 16ABR8 | `27c6:55b4` | Goodix GF3268 | Working | [entry](../devices/27c6:55b4/) |
| Lenovo ThinkPad E14 Gen 5 | `10a5:9800` | FPC Match-on-Host / fpcmoh | Working | [entry](../devices/10a5:9800/) |
| Lenovo ThinkBook | `27c6:550a` | Goodix 550a - vendor TOD blob route | Working (vendor blob) | [entry](../devices/27c6:550a/) |
| Lenovo ThinkPad E14 | `27c6:550a` | Goodix 550a - vendor TOD blob route | Working (vendor blob) | [entry](../devices/27c6:550a/) |
| Lenovo ThinkPad E14 Gen 4 | `04f3:0c4b` | ELAN 0c4b - Lenovo TOD blob route | Working (vendor blob) | [entry](../devices/04f3:0c4b/) |
| Lenovo ThinkPad E15 | `27c6:550a` | Goodix 550a - vendor TOD blob route | Working (vendor blob) | [entry](../devices/27c6:550a/) |
| Lenovo ThinkPad T480 | `138a:0097` | Validity/Synaptics VFS0097 (VCSFW) | WIP | [entry](../devices/138a:0097/) |
| Lenovo ThinkPad T480s | `138a:0097` | Validity/Synaptics VFS0097 (VCSFW) | WIP | [entry](../devices/138a:0097/) |
| Lenovo ThinkPad T580 | `138a:0097` | Validity/Synaptics VFS0097 (VCSFW) | WIP | [entry](../devices/138a:0097/) |
| Lenovo ThinkPad X1 Carbon Gen 6 | `138a:0097` | Validity/Synaptics VFS0097 (VCSFW) | WIP | [entry](../devices/138a:0097/) |
| Ideapad 5 | `27c6:55a2` | - | No known fix | [gap-map](unsupported-devices.md) |
| Lenovo IdeaPad 3-15ARE05 | `04f3:0c57` | - | No known fix | [gap-map](unsupported-devices.md) |
| Lenovo Thinkbook 15 G13 | `06cb:00fd` | - | No known fix | [gap-map](unsupported-devices.md) |
| Lenovo ThinkPad E14 | `27c6:5503` | - | No known fix | [gap-map](unsupported-devices.md) |
| lenovo Yoga 720 | `06cb:0081` | - | No known fix | [gap-map](unsupported-devices.md) |
| Lenovo Yoga 9 14IAP7 | `27c6:550c` | - | No known fix | [gap-map](unsupported-devices.md) |
| Lenovo Yoga 9i 14ITL | `0bda:5812` | - | No known fix | [gap-map](unsupported-devices.md) |
| Thinkpad C740, Yoga | `06cb:00be` | lead: RE effort exists | No known fix | [gap-map](unsupported-devices.md) |
| ThinkPad E14 | `06cb:00da` | - | No known fix | [gap-map](unsupported-devices.md) |
| Thinkpad E14 / Thinkbook 13s-IWL | `27c6:55a4` | - | No known fix | [gap-map](unsupported-devices.md) |
| yoga 730-13IWL 81JR | `27c6:5584` | - | No known fix | [gap-map](unsupported-devices.md) |

## Dell

| Laptop model | USB ID | Sensor | Status | Where to go |
|--------------|--------|--------|--------|-------------|
| Dell XPS 13 7390 2-in-1 | `27c6:5385` | Goodix HTK32 | Working | [entry](../devices/27c6:5385/) |
| Dell XPS 13 9305 | `27c6:5385` | Goodix HTK32 | Working | [entry](../devices/27c6:5385/) |
| Dell XPS 15 9570 | `27c6:5385` | Goodix HTK32 | Working | [entry](../devices/27c6:5385/) |
| Dell XPS 13 9300 | `27c6:533c` | Goodix 533c - Dell OEM TOD blob route | Working (vendor blob) | [entry](../devices/27c6:533c/) |
| Dell XPS 15 9500 | `27c6:533c` | Goodix 533c - Dell OEM TOD blob route | Working (vendor blob) | [entry](../devices/27c6:533c/) |
| Dell Latitude 7300 | `broadcom-controlvault3` | Broadcom ControlVault3 (Dell) | WIP | [entry](../devices/broadcom-controlvault3/) |
| Dell G5 15 5590 | `27c6:530c` | - | No known fix | [gap-map](unsupported-devices.md) |
| Dell Inspiron 17 7000 | `27c6:538c` | - | No known fix | [gap-map](unsupported-devices.md) |
| Dell Inspiron 17 7000 | `27c6:538d` | - | No known fix | [gap-map](unsupported-devices.md) |
| Dell Latitude 3490 | `138a:00a6` | - | No known fix | [gap-map](unsupported-devices.md) |
| dell latitude 7200 | `06cb:00bc` | - | No known fix | [gap-map](unsupported-devices.md) |
| Dell Latitude 7300 | `0a5c:5843` | - | No known fix | [gap-map](unsupported-devices.md) |
| Dell Latitude 7480 | `0a5c:5834` | - | No known fix | [gap-map](unsupported-devices.md) |
| Dell Latitude e5470 | `0a5c:5805` | - | No known fix | [gap-map](unsupported-devices.md) |
| Dell Latitude E6530 | `0a5c:5801` | - | No known fix | [gap-map](unsupported-devices.md) |
| Dell Precision 7550 | `0a5c:5842` | - | No known fix | [gap-map](unsupported-devices.md) |
| Dell Precision M4800 | `0a5c:5802` | - | No known fix | [gap-map](unsupported-devices.md) |
| Dell XPS 13 7390 2-in-1 | `27c6:532d` | - | No known fix | [gap-map](unsupported-devices.md) |
| Dell XPS 9315 2-in-1 | `27c6:6382` | - | No known fix | [gap-map](unsupported-devices.md) |

## HP

| Laptop model | USB ID | Sensor | Status | Where to go |
|--------------|--------|--------|--------|-------------|
| HP EliteBook | `06cb:00ff` | Synaptics Tudor match-in-sensor family | Working | [entry](../devices/06cb:00ff/) |
| HP Envy | `06cb:00ff` | Synaptics Tudor match-in-sensor family | Working | [entry](../devices/06cb:00ff/) |
| HP ProBook | `06cb:00ff` | Synaptics Tudor match-in-sensor family | Working | [entry](../devices/06cb:00ff/) |
| HP Spectre | `06cb:00ff` | Synaptics Tudor match-in-sensor family | Working | [entry](../devices/06cb:00ff/) |
| HP Pavilion x360 14-dh | `06cb:00cb` | Validity/Synaptics VCSFW 0x969 | WIP | [entry](../devices/06cb:00cb/) |
| HP ProBook 450 G6 | `06cb:00b7` | Validity/Synaptics VCSFW 0xd51 | WIP | [entry](../devices/06cb:00b7/) |
| HP ZBook 17 G6 | `06cb:00b7` | Validity/Synaptics VCSFW 0xd51 | WIP | [entry](../devices/06cb:00b7/) |
| HP ZBook Studio x360 G5 | `138a:00ab` | Validity/Synaptics VCSFW 0x969 | WIP | [entry](../devices/138a:00ab/) |
| HP 640 G4 Notebook | `138a:003a` | - | No known fix | [gap-map](unsupported-devices.md) |
| HP EliteBook 1040 G4 | `138a:0092` | - | No known fix | [gap-map](unsupported-devices.md) |
| HP EliteBook 8560w | `138a:003c` | - | No known fix | [gap-map](unsupported-devices.md) |
| HP EliteBook 8770w | `138a:003d` | - | No known fix | [gap-map](unsupported-devices.md) |
| HP ProBook 430 G7 | `06cb:00d8` | - | No known fix | [gap-map](unsupported-devices.md) |
| HP Probook 450 G8 | `04f3:0c5e` | - | No known fix | [gap-map](unsupported-devices.md) |
| HP Spectre x360 - 13 -ap0xxxxx | `06cb:00bb` | - | No known fix | [gap-map](unsupported-devices.md) |
| HP Zbook 15 G2 / HP Probook 430 | `138a:003f` | - | No known fix | [gap-map](unsupported-devices.md) |

## Asus

| Laptop model | USB ID | Sensor | Status | Where to go |
|--------------|--------|--------|--------|-------------|
| ASUS Vivobook f571gt- al318t | `04f3:3104` | lead: partial | No known fix | [gap-map](unsupported-devices.md) |
| Asus Vivobook K6500zc | `2808:a658` | - | No known fix | [gap-map](unsupported-devices.md) |
| ASUS VivoBook Pro 15 N580GD | `04f3:3057` | - | No known fix | [gap-map](unsupported-devices.md) |
| Asus Zenbook Pro UX580 | `04f3:2706` | - | No known fix | [gap-map](unsupported-devices.md) |
| ASUS ZenBook S UX391FA-AH001T | `27c6:5201` | - | No known fix | [gap-map](unsupported-devices.md) |
| ASUS ZenBook UX330CA | `04f3:3032` | - | No known fix | [gap-map](unsupported-devices.md) |
| ELAN:ARM-M4 ASUS Vivobook | `04f3:0c90` | - | No known fix | [gap-map](unsupported-devices.md) |
| Focaltech FT9365, Asus VivoBook | `2808:a553` | - | No known fix | [gap-map](unsupported-devices.md) |

## Acer

| Laptop model | USB ID | Sensor | Status | Where to go |
|--------------|--------|--------|--------|-------------|
| Acer ConceptD CC314-72 | `06cb:00e4` | - | No known fix | [gap-map](unsupported-devices.md) |
| Acer Spin 3, SP313-51N | `06cb:00dc` | - | No known fix | [gap-map](unsupported-devices.md) |
| Acer Swift 1 (SF114-32-P78E)? | `1c7a:0300` | lead: RE effort exists | No known fix | [gap-map](unsupported-devices.md) |
| Acer Swift 3 | `04f3:0c7f` | - | No known fix | [gap-map](unsupported-devices.md) |
| Acer Swift 3 OLED (SF314-71-56U3) | `10a5:e340` | - | No known fix | [gap-map](unsupported-devices.md) |
| Acer Swift 3 SF314-43 | `04f3:0c72` | - | No known fix | [gap-map](unsupported-devices.md) |
| ELAN:ARM-M4 ACER Aspire Vero | `04f3:0c85` | - | No known fix | [gap-map](unsupported-devices.md) |

## Samsung

| Laptop model | USB ID | Sensor | Status | Where to go |
|--------------|--------|--------|--------|-------------|
| Samsung Galaxy Book 4 | `2808:6553` | FocalTech FT9365 ESS (focaltech_moc) | Merged upstream | [entry](../devices/2808:6553/) |
| Samsung GalaxyBook Pro 360 | `1c7a:057e` | - | No known fix | [gap-map](unsupported-devices.md) |

## Huawei

| Laptop model | USB ID | Sensor | Status | Where to go |
|--------------|--------|--------|--------|-------------|
| MagicBook 2019 R7 / Huawei Matebook 13 2020 | `27c6:5117` | - | No known fix | [gap-map](unsupported-devices.md) |
| Matebook D16 | `27c6:5120` | - | No known fix | [gap-map](unsupported-devices.md) |

## Honor

| Laptop model | USB ID | Sensor | Status | Where to go |
|--------------|--------|--------|--------|-------------|
| HONOR HYM-WXX MagicBook 16 | `27c6:5125` | - | No known fix | [gap-map](unsupported-devices.md) |
| Honor Magicbook Art 14 | `27c6:5f91` | - | No known fix | [gap-map](unsupported-devices.md) |
| Honor Magicbook x16 plus 2024 | `10a5:a921` | - | No known fix | [gap-map](unsupported-devices.md) |
| Honor MagicBook X16Pro Ryzen 7 7840HS | `27c6:5f10` | - | No known fix | [gap-map](unsupported-devices.md) |

## Xiaomi / Redmi

| Laptop model | USB ID | Sensor | Status | Where to go |
|--------------|--------|--------|--------|-------------|
| Xiaomi RedmiBook 14 Pro | `10a5:9201` | FPC Sensor Controller L:0001 - fingerprint-ocv | Working (vendor blob) | [entry](../devices/10a5:9201/) |
| Mi RedmiBook 15 2022 Pro | `27c6:589a` | - | No known fix | [gap-map](unsupported-devices.md) |
| Mi RedmiBook Pro | `27c6:581a` | - | No known fix | [gap-map](unsupported-devices.md) |
| Redmi Book Pro, 14" AMD | `04f3:0c70` | - | No known fix | [gap-map](unsupported-devices.md) |

## Microsoft Surface

| Laptop model | USB ID | Sensor | Status | Where to go |
|--------------|--------|--------|--------|-------------|
| ELAN:ARM-M4 - Surface Laptop Go 2 | `04f3:0c80` | - | No known fix | [gap-map](unsupported-devices.md) |
| Surface Laptop Go | `04f3:0c5a` | - | No known fix | [gap-map](unsupported-devices.md) |

## MSI

| Laptop model | USB ID | Sensor | Status | Where to go |
|--------------|--------|--------|--------|-------------|
| MSI Prestige 14 A10RB | `06cb:009b` | - | No known fix | [gap-map](unsupported-devices.md) |

## LG

| Laptop model | USB ID | Sensor | Status | Where to go |
|--------------|--------|--------|--------|-------------|
| LG GRAM 2018 | `10a5:0007` | - | No known fix | [gap-map](unsupported-devices.md) |

## Handhelds and mini PCs

| Laptop model | USB ID | Sensor | Status | Where to go |
|--------------|--------|--------|--------|-------------|
| AYANEO 2 | `2541:0236` | Chipsailing CS9711 | Working (vendor blob) | [entry](../devices/2541:0236/) |
| GPD Win Max 2 | `2541:0236` | Chipsailing CS9711 | Working (vendor blob) | [entry](../devices/2541:0236/) |
| Chuwi MiniBook X | `mafp8800` | Microarray MAFP8800 (SPI) | WIP | [entry](../devices/mafp8800/) |
| GPD MicroPC 2 | `mafp8800` | Microarray MAFP8800 (SPI) | WIP | [entry](../devices/mafp8800/) |
| GTR5 mini | `1c7a:0577` | - | No known fix | [gap-map](unsupported-devices.md) |

## Other vendors

| Laptop model | USB ID | Sensor | Status | Where to go |
|--------------|--------|--------|--------|-------------|
| CanvasBio CB2000 | `2df0:0003` | - | No known fix | [gap-map](unsupported-devices.md) |
| Clevo Laptops | `06cb:00a8` | - | No known fix | [gap-map](unsupported-devices.md) |
| realme book MP | `27c6:5e0a` | - | No known fix | [gap-map](unsupported-devices.md) |
| Teclast F6 Pro | `27c6:5740` | - | No known fix | [gap-map](unsupported-devices.md) |
| Toshiba B2B-range X30-D and X40-D | `06cb:008a` | - | No known fix | [gap-map](unsupported-devices.md) |

## Other and unidentified

Rows the upstream wiki records against a chip or module name
rather than a machine. Match these on the USB ID.

| Laptop model | USB ID | Sensor | Status | Where to go |
|--------------|--------|--------|--------|-------------|
| Broadcom Corp. 58200 | `0a5c:5864` | - | No known fix | [gap-map](unsupported-devices.md) |
| DigitalPersona 5300 | `05ba:000e` | - | No known fix | [gap-map](unsupported-devices.md) |
| ELAN/FA461D-2203 | `04f3:3128` | - | No known fix | [gap-map](unsupported-devices.md) |
| External, Validity90 project is relevant | `06cb:0088` | - | No known fix | [gap-map](unsupported-devices.md) |
| magikbook 14x | `10a5:a900` | - | No known fix | [gap-map](unsupported-devices.md) |
| Validity90 | `06cb:00a1` | - | No known fix | [gap-map](unsupported-devices.md) |
| Validity90 | `06cb:00a2` | - | No known fix | [gap-map](unsupported-devices.md) |

---

_Generated by `tools/gen-laptop-index.py`. Do not edit by hand: edit a
`devices/<id>/MODELS` file or the gap-map and regenerate._
