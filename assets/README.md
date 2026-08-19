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

The glyph is deliberately coarse: three ridges, stroke and gap both about
2.9 units on the 32-unit tile, sized so the outer ridge nearly touches the
edge. Favicons are read at 16-24 px, where the stroke is barely a pixel
wide, so any extra ridge or padding turns the whole thing into grey mush.
An earlier version used the full nine-path Lucide `fingerprint` icon inset
in the tile; it was illegible below 32 px. Keep the ridge count and the
generous gaps if you edit this.

## Attribution

The fingerprint glyph is original to this repository.
