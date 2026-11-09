# Mass Reaction — website art direction

A mysterious abandoned laboratory: dark metal, aged brass, pipes, amber lamps, green glow, and the feeling of a machine that was never switched off. A light corporate look was rejected. The name and the mechanics are about mass and balance; the game has no molecules, but that does not rule out the laboratory setting.

## Assets

`dist/assets/laboratory-v2.webp` is a background generated with the built-in ImageGen from a style reference; it is not a game screenshot. The screenshots in `dist/assets/screens/` are real frames of the game in the Alchemy skin on iPhone 17 Pro Max. The special balls in `dist/assets/specials/` and the app icon come from the game's resources; see the README for how to rebuild them. `grain.svg` is a light procedural texture, and `favicon.svg` is the scales mark in the site palette. Screenshots sit in a CSS phone frame (`.phone`) in the same tones as the brass frames.

The early apparatus concept art and the PNG original of the background are kept locally in `art-source/` and are no longer used on the site.

The font is Barlow Condensed ExtraBold from the official [Google Fonts](https://github.com/google/fonts/tree/main/ofl/barlowcondensed) repository, under the SIL OFL (`dist/assets/fonts/OFL.txt`). It is served with the site.

## Background prompt (ImageGen)

```text
Use case: stylized-concept.
Asset type: cinematic wide background artwork for a game website, 16:9 landscape, high resolution.
Input image 1 is a STYLE AND MATERIAL REFERENCE ONLY, not an edit target and not a website screenshot.
Create an immersive mysterious abandoned industrial physics laboratory in the exact material world of the reference: almost black iron, old soot-dark brass, riveted steel, scratched glass, dense weathered pipework, a faint green light inside one old glass chamber, small warm amber tungsten lamps, oily worn surfaces, dust and a little suspended steam. No people. The room has been abandoned, yet a few mechanisms and indicator lamps remain powered. Rich tangible material detail, realistic cinematic game environment, heavy shadows and believable ageing. Restrained green, rich amber highlights, charcoal and tarnished bronze; no clean white surfaces.
Composition: panoramic wide interior, straight-on view into a bench-and-machinery area. Dense pipes at the extreme left and right edges. LEFT HALF must be deeply shadowed negative space for separately rendered live website typography, with dark subtle wall texture rather than pitch-black empty background. RIGHT HALF and far background carry the luminous instrument details; leave a shadowed vertical recess on the right where the actual game concept artwork can be overlaid in HTML. The lower edge dissolves naturally into dark floor and mist. The center should have depth, not a flat wallpaper.
Avoid all readable words, letters, numbers, logos, typography, website UI, buttons, screens with text, game balls, molecular icons, floating neon sci-fi HUDs, cartoon gears, fantasy creatures, people, cozy workshop lighting, polished showroom materials. Do not recreate the puzzle board. This is the surrounding abandoned laboratory itself.
```
