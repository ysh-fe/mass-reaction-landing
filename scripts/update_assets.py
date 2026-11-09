#!/usr/bin/env python3
"""Rebuild the site's game images from the Mass Reaction game repository.

Usage: python3 scripts/update_assets.py <path-to-game-repo> [device-check-label]

Takes the iPhone 17 Pro Max shots made by `tools/device-check/devicecheck.sh capture <label>`
(default label: after), the special-ball art and the app icon, and writes web-sized copies
into dist/assets/. Needs Pillow: pip3 install pillow.
"""
import pathlib
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

SITE = pathlib.Path(__file__).resolve().parent.parent
ASSETS = SITE / "dist" / "assets"

SCREENS = ["game", "filled", "offer", "gameover"]
SPECIALS = {
    "SilverStar": "silver-star",
    "GoldStar": "gold-star",
    "CopperHeart": "heart",
    "StashJoker": "joker",
    "MysteryQuestion": "mystery",
    "StashBomb": "bomb",
    "StashCutter": "cutter",
    "ColourZap": "colour-zap",
    "Tint": "tint",
    "Flash": "flash",
    "ColourJoker": "colour-joker",
    "DiagonalZap": "diagonal-zap",
    "TopZap": "top-zap",
    "BottomTint": "bottom-tint",
    "DiagonalFlash": "diagonal-flash",
    "ColourBomb": "colour-bomb",
    "HorizontalZap": "horizontal-zap",
    "MulticolourZap": "multicolour-zap",
    "Tint3x3": "tint-3x3",
    "TriangleFlash": "triangle-flash",
}


def screens(game: pathlib.Path, label: str) -> None:
    out = ASSETS / "screens"
    out.mkdir(exist_ok=True)
    for name in SCREENS:
        im = Image.open(game / "docs/device-check" / label / f"iphone-17-pro-max--{name}.png").convert("RGB")
        w = 720
        im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(
            out / f"{name}.jpg", quality=84, optimize=True, progressive=True)


def specials(game: pathlib.Path) -> None:
    out = ASSETS / "specials"
    out.mkdir(exist_ok=True)
    art = game / "BoardKit/Sources/BoardKit/Resources/Alchemy"
    for source, name in SPECIALS.items():
        im = Image.open(art / f"{source}.png").convert("RGBA")
        im = im.crop(im.getbbox())
        side = max(im.size)
        square = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        square.paste(im, ((side - im.width) // 2, (side - im.height) // 2))
        square.resize((112, 112), Image.LANCZOS).save(out / f"{name}.png", optimize=True)


def icons(game: pathlib.Path) -> None:
    icon = Image.open(game / "App/Assets.xcassets/AppIcon.appiconset/AppIcon.png").convert("RGB")
    icon.resize((180, 180), Image.LANCZOS).save(ASSETS / "apple-touch-icon.png", optimize=True)
    icon.resize((160, 160), Image.LANCZOS).save(ASSETS / "app-icon.png", optimize=True)


def share_image() -> None:
    bg = Image.open(ASSETS / "laboratory-v2.jpg").convert("RGB")
    bg = bg.resize((1200, round(bg.height * 1200 / bg.width)), Image.LANCZOS)
    top = max(0, (bg.height - 630) // 2)
    bg = ImageEnhance.Brightness(bg.crop((0, top, 1200, top + 630))).enhance(0.55)
    shade = Image.new("RGBA", (1200, 630), (9, 11, 9, 0))
    draw = ImageDraw.Draw(shade)
    for x in range(1200):
        draw.line([(x, 0), (x, 630)], fill=(9, 11, 9, int(200 * max(0, 1 - x / 700))))
    og = Image.alpha_composite(bg.convert("RGBA"), shade)

    shot = Image.open(ASSETS / "screens/game.jpg").convert("RGB")
    ph = 560
    pw = round(shot.width * ph / shot.height)
    shot = shot.resize((pw, ph), Image.LANCZOS)
    frame = Image.new("RGBA", (pw + 16, ph + 16), (0, 0, 0, 0))
    ImageDraw.Draw(frame).rounded_rectangle(
        [0, 0, pw + 15, ph + 15], radius=44, fill=(28, 26, 20, 255), outline=(139, 112, 68, 255), width=2)
    mask = Image.new("L", (pw, ph), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, pw - 1, ph - 1], radius=36, fill=255)
    frame.paste(shot, (8, 8), mask)
    glow = Image.new("RGBA", og.size, (0, 0, 0, 0))
    ImageDraw.Draw(glow).rounded_rectangle([1200 - pw - 130, 25, 1200 - 90, 605], radius=50, fill=(0, 0, 0, 170))
    og = Image.alpha_composite(og, glow.filter(ImageFilter.GaussianBlur(18)))
    og.alpha_composite(frame, (1200 - pw - 108, (630 - ph - 16) // 2))

    font_path = str(ASSETS / "fonts/barlow-condensed-extrabold.ttf")
    big = ImageFont.truetype(font_path, 150)
    small = ImageFont.truetype(font_path, 34)
    text = ImageDraw.Draw(og)
    text.text((70, 120), "MASS", font=big, fill=(221, 212, 186))
    text.text((70, 265), "REACTION", font=big, fill=(203, 164, 99))
    text.text((74, 450), "AN ENDLESS BALANCE PUZZLE FOR IPHONE", font=small, fill=(176, 170, 146))
    og.convert("RGB").save(ASSETS / "og-image.jpg", quality=86, optimize=True)


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    game = pathlib.Path(sys.argv[1]).expanduser().resolve()
    label = sys.argv[2] if len(sys.argv) > 2 else "after"
    screens(game, label)
    specials(game)
    icons(game)
    share_image()
    print("Updated images in", ASSETS)


if __name__ == "__main__":
    main()
