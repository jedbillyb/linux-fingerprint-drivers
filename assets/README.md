# Site icons

`favicon.svg` is the source; `favicon.ico` and `apple-touch-icon.png` are
rendered from it and committed so the site build needs no image tooling.

To regenerate the raster versions after editing the SVG:

```sh
magick -background none assets/favicon.svg -define icon:auto-resize=64,48,32,16 assets/favicon.ico
magick -background none assets/favicon.svg -resize 180x180 -strip PNG32:assets/apple-touch-icon.png
```

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
