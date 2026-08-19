# Site icons

`favicon.svg` is the source; `favicon.ico`, `apple-touch-icon.png`,
`icon-192.png` and `icon-512.png` are rendered from it and committed so the
site build needs no image tooling. The two large PNGs exist for Google, which
caches one raster copy of a site's favicon and upscales it everywhere it is
shown, so a big source is worth having even though no browser needs it.

To regenerate the raster versions after editing the SVG:

```sh
# The SVG carries a viewBox but no width/height, so ImageMagick rasterises it
# at 32x32 and everything larger becomes an upscale of that. -density forces a
# native render: 96 dpi is the 32-unit viewBox 1:1, so scale it by target/32.
magick -background none -density 1536 assets/favicon.svg -define icon:auto-resize=64,48,32,16 assets/favicon.ico
magick -background none -density 1536 assets/favicon.svg -strip PNG32:assets/icon-512.png
magick -background none -density 576 assets/favicon.svg -strip PNG32:assets/icon-192.png
magick -background none -density 540 assets/favicon.svg -strip PNG32:assets/apple-touch-icon.png
```

Check the result really was rendered and not upscaled: a native 512 render has
a few hundred distinct colours, an upscaled one has thousands of near-duplicate
blues.

## Legibility

The glyph is a dense one, so two things keep it readable and both are easy to
undo by accident:

- It is scaled to fill the tile. The `translate(1.978,1.978) scale(1.1685)`
  on the group grows the Lucide artwork from a 22.25-unit ink box to 26 units
  on the 32-unit tile, which widens the gaps between ridges by the same
  factor. `stroke-width` is divided by that scale so the strokes still render
  at 2.4 units; raising it back to 2.4 would close the gaps again.
- It must be rendered, not upscaled. See the `-density` note above.

Even so, expect it to soften below about 24 px, which is a browser tab. That
is the cost of nine ridges and it was accepted deliberately.

## Attribution

The fingerprint glyph is the `fingerprint` icon from
[Lucide](https://lucide.dev), used unmodified except for stroke width,
colour and a uniform scale, on a solid tile.

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
