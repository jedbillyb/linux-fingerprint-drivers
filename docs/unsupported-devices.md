# Devices with no known fix (contributor gap-map)

The 104 USB fingerprint sensors below are on the official libfprint
[Unsupported Devices](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Unsupported-Devices)
list and have **no working driver here or upstream**. Devices already covered by
an entry in [`devices/`](../devices/) (working or WIP) are omitted - check the
[main README](../README.md) tables first. This is a contributor gap-map: if you
have one of these, a protocol dump or a driver is welcome.

"Lead" flags a known reverse-engineering effort, partial result, or WIP/PoC
noted on the wiki; follow the device's wiki page for links.

Source: libfprint wiki, fetched 2026-06-18. Rows are removed as devices gain
an entry; last reconciled 2026-07-26.

Two clusters listed below do now have WIP driver work tracked in the README:
the Dell **`0a5c:58xx` Broadcom** family is targeted by the ControlVault3 driver
(MR [!620](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/620),
[entry](../devices/broadcom-controlvault3/)), and **`138a:009d`** by the Validity
VCSFW driver (MR [!579](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/579),
[entry](../devices/138a:0097/)).

| USB ID | Hardware | Lead |
|--------|----------|------|
| [047d:00f2](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/047d:00f2) | External (USB) |  |
| [047d:8054](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/047d:8054) | External (USB) |  |
| [047d:8055](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/047d:8055) | External (USB) |  |
| [04f3:036b](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/04f3:036b) | - |  |
| [04f3:0c57](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/04f3:0c57) | Lenovo IdeaPad 3-15ARE05 |  |
| [04f3:0c5a](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/04f3:0c5a) | Surface Laptop Go |  |
| [04f3:0c5e](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/04f3:0c5e) | HP Probook 450 G8 |  |
| [04f3:0c60](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/04f3:0c60) | Lenovo Optical Mouse |  |
| [04f3:0c70](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/04f3:0c70) | Redmi Book Pro, 14" AMD |  |
| [04f3:0c72](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/04f3:0c72) | Acer Swift 3 SF314-43 |  |
| [04f3:0c77](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/04f3:0c77) | - | partial |
| [04f3:0c7c](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/04f3:0c7c) | - | WIP/PoC upstream |
| [04f3:0c7f](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/04f3:0c7f) | Acer Swift 3 |  |
| [04f3:0c80](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/04f3:0c80) | ELAN:ARM-M4 - Surface Laptop Go 2 |  |
| [04f3:0c85](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/04f3:0c85) | ELAN:ARM-M4 ACER Aspire Vero |  |
| [04f3:0c8a](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/04f3:0c8a) | - |  |
| [04f3:0c90](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/04f3:0c90) | ELAN:ARM-M4 ASUS Vivobook |  |
| [04f3:2706](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/04f3:2706) | Asus Zenbook Pro UX580 |  |
| [04f3:3032](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/04f3:3032) | ASUS ZenBook UX330CA |  |
| [04f3:3057](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/04f3:3057) | ASUS VivoBook Pro 15 N580GD |  |
| [04f3:3104](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/04f3:3104) | ASUS Vivobook f571gt- al318t | partial |
| [04f3:3128](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/04f3:3128) | ELAN/FA461D-2203 |  |
| [05ba:000e](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/05ba:000e) | DigitalPersona 5300 |  |
| [06cb:0051](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/06cb:0051) | - |  |
| [06cb:0081](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/06cb:0081) | lenovo Yoga 720 |  |
| [06cb:0088](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/06cb:0088) | External, Validity90 project is relevant |  |
| [06cb:008a](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/06cb:008a) | Toshiba B2B-range X30-D and X40-D |  |
| [06cb:009b](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/06cb:009b) | MSI Prestige 14 A10RB |  |
| [06cb:00a1](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/06cb:00a1) | Validity90 |  |
| [06cb:00a2](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/06cb:00a2) | Validity90 |  |
| [06cb:00a8](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/06cb:00a8) | Clevo Laptops |  |
| [06cb:00bb](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/06cb:00bb) | HP Spectre x360 - 13 -ap0xxxxx |  |
| [06cb:00bc](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/06cb:00bc) | dell latitude 7200 |  |
| [06cb:00be](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/06cb:00be) | Thinkpad C740, Yoga | RE effort exists |
| [06cb:00d8](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/06cb:00d8) | HP ProBook 430 G7 |  |
| [06cb:00da](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/06cb:00da) | ThinkPad E14 |  |
| [06cb:00dc](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/06cb:00dc) | Acer Spin 3, SP313-51N |  |
| [06cb:00e4](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/06cb:00e4) | Acer ConceptD CC314-72 |  |
| [06cb:00fd](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/06cb:00fd) | Lenovo Thinkbook 15 G13 |  |
| [0a5c:5801](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/0a5c:5801) | Dell Latitude E6530 |  |
| [0a5c:5802](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/0a5c:5802) | Dell Precision M4800 |  |
| [0a5c:5805](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/0a5c:5805) | Dell Latitude e5470 |  |
| [0a5c:5834](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/0a5c:5834) | Dell Latitude 7480 |  |
| [0a5c:5840](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/0a5c:5840) | - |  |
| [0a5c:5841](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/0a5c:5841) | - |  |
| [0a5c:5842](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/0a5c:5842) | Dell Precision 7550 |  |
| [0a5c:5843](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/0a5c:5843) | Dell Latitude 7300 |  |
| [0a5c:5844](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/0a5c:5844) | - |  |
| [0a5c:5845](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/0a5c:5845) | - |  |
| [0a5c:5860](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/0a5c:5860) | - |  |
| [0a5c:5863](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/0a5c:5863) | - |  |
| [0a5c:5864](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/0a5c:5864) | Broadcom Corp. 58200 |  |
| [0a5c:5865](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/0a5c:5865) | - |  |
| [0a5c:5866](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/0a5c:5866) | - |  |
| [0a5c:5867](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/0a5c:5867) | - |  |
| [0bda:5812](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/0bda:5812) | Lenovo Yoga 9i 14ITL |  |
| [10a5:0007](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/10a5:0007) | LG GRAM 2018 |  |
| [10a5:a120](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/10a5:a120) | - |  |
| [10a5:a900](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/10a5:a900) | magikbook 14x |  |
| [10a5:a921](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/10a5:a921) | Honor Magicbook x16 plus 2024 |  |
| [10a5:e340](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/10a5:e340) | Acer Swift 3 OLED (SF314-71-56U3) |  |
| [1188:9545](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/1188:9545) | - |  |
| [138a:0007](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/138a:0007) | - |  |
| [138a:003a](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/138a:003a) | HP 640 G4 Notebook |  |
| [138a:003c](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/138a:003c) | HP EliteBook 8560w |  |
| [138a:003d](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/138a:003d) | HP EliteBook 8770w |  |
| [138a:003f](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/138a:003f) | HP Zbook 15 G2 / HP Probook 430 |  |
| [138a:0092](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/138a:0092) | HP EliteBook 1040 G4 |  |
| [138a:0094](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/138a:0094) | - |  |
| [138a:009d](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/138a:009d) | - |  |
| [138a:00a6](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/138a:00a6) | Dell Latitude 3490 |  |
| [1491:0088](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/1491:0088) | - |  |
| [16d1:1027](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/16d1:1027) | - |  |
| [1c7a:0300](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/1c7a:0300) | Acer Swift 1 (SF114-32-P78E)? | RE effort exists |
| [1c7a:0577](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/1c7a:0577) | GTR5 mini |  |
| [1c7a:057e](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/1c7a:057e) | Samsung GalaxyBook Pro 360 |  |
| [27c6:5042](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/27c6:5042) | External |  |
| [27c6:5117](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/27c6:5117) | MagicBook 2019 R7 / Huawei Matebook 13 2020 |  |
| [27c6:5120](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/27c6:5120) | Matebook D16 |  |
| [27c6:5125](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/27c6:5125) | HONOR HYM-WXX MagicBook 16 |  |
| [27c6:5201](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/27c6:5201) | ASUS ZenBook S UX391FA-AH001T |  |
| [27c6:5301](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/27c6:5301) | - |  |
| [27c6:530c](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/27c6:530c) | Dell G5 15 5590 |  |
| [27c6:532d](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/27c6:532d) | Dell XPS 13 7390 2-in-1 |  |
| [27c6:5381](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/27c6:5381) | - |  |
| [27c6:538c](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/27c6:538c) | Dell Inspiron 17 7000 |  |
| [27c6:538d](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/27c6:538d) | Dell Inspiron 17 7000 |  |
| [27c6:5503](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/27c6:5503) | Lenovo ThinkPad E14 |  |
| [27c6:550c](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/27c6:550c) | Lenovo Yoga 9 14IAP7 |  |
| [27c6:5584](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/27c6:5584) | yoga 730-13IWL 81JR |  |
| [27c6:55a2](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/27c6:55a2) | Ideapad 5 |  |
| [27c6:55a4](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/27c6:55a4) | Thinkpad E14 / Thinkbook 13s-IWL |  |
| [27c6:5740](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/27c6:5740) | Teclast F6 Pro |  |
| [27c6:581a](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/27c6:581a) | Mi RedmiBook Pro |  |
| [27c6:589a](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/27c6:589a) | Mi RedmiBook 15 2022 Pro |  |
| [27c6:5e0a](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/27c6:5e0a) | realme book MP |  |
| [27c6:5f10](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/27c6:5f10) | Honor MagicBook X16Pro Ryzen 7 7840HS |  |
| [27c6:5f91](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/27c6:5f91) | Honor Magicbook Art 14 |  |
| [27c6:6382](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/27c6:6382) | Dell XPS 9315 2-in-1 |  |
| [2808:9348](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/2808:9348) | - |  |
| [2808:a553](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/2808:a553) | Focaltech FT9365, Asus VivoBook |  |
| [2808:a658](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/2808:a658) | Asus Vivobook K6500zc |  |
| [2df0:0003](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/2df0:0003) | CanvasBio CB2000 |  |
| [3538:0930](https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Devices/3538:0930) | External |  |

_SPI sensors (ELAN7001/7002/079C, GXFP5187/51B7, GDIX51C0, fpc1020, etc.) are
also unsupported; see the wiki's SPI Devices section._
