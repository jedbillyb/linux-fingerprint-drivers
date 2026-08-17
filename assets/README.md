# Site icons

`favicon.svg` is the source; `favicon.ico` and `apple-touch-icon.png` are
rendered from it and committed so the site build needs no image tooling.

To regenerate the raster versions after editing the SVG:

```sh
magick -background none assets/favicon.svg -define icon:auto-resize=48,32,16 assets/favicon.ico
magick -background none assets/favicon.svg -resize 180x180 -strip PNG8:assets/apple-touch-icon.png
```

## Attribution

The fingerprint glyph is the `fingerprint` icon from
[Lucide](https://lucide.dev), used unmodified except for stroke width and
colour, on a solid tile.

Lucide is ISC licensed:

> Copyright (c) 2020, Lucide Contributors
>
> Permission to use, copy, modify, and/or distribute this software for any
> purpose with or without fee is hereby granted, provided that the above
> copyright notice and this permission notice appear in all copies.

Lucide derives from [Feather](https://github.com/feathericons/feather)
(MIT, Copyright (c) 2013-2017 Cole Bemis). ISC and MIT are both compatible
with this repository's LGPL-2.1 licensing; see the root
[LICENSE](../LICENSE) for the code terms.
