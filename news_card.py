#!/usr/bin/env python3
"""GunnerWired news poster, standalone: needs only this file, the two fonts and Pillow.

python3 news_card.py --title "TEAM NEWS" --kicker "Team news" \
    --headline "Saka back in training" --sub "Fit for Newcastle on Saturday" \
    --style home --out card.png

Design rules: DESIGN.md. Fonts: LeagueGothic.ttf and Poppins-Medium.ttf next to this file.
"""
import argparse
import base64
import io
import os
import subprocess
import sys

CHANNEL = "@GunnerWired"
TEAM_ID = 57
CARDS = True
DRY_RUN = False
CARD_FONT_DISPLAY = "LeagueGothic.ttf"
CARD_FONT_SMALL = "Poppins-Medium.ttf"


def log(msg):
    print(msg, file=sys.stderr, flush=True)


def is_home(match):
    return match["homeTeam"].get("id") == TEAM_ID


# ----------------------------------------------------------------------------
# Picture cards: portrait posters (see DESIGN.md)
# ----------------------------------------------------------------------------
CARD_W, CARD_H = 1080, 1350
CARD_SS = 2                       # drawn at 2x then scaled down, for smooth edges
CARD_TEXT = (255, 255, 255)
CARD_ACCENT = (255, 204, 0)
CARD_STYLES = {
    "home": {"bg": (100, 7, 22), "bolt": (206, 17, 38)},     # deep red, red bolts
    "away": {"bg": (15, 24, 56), "bolt": (34, 64, 150)},     # navy, blue bolts
}
# Bolt pattern geometry, in pattern units (locked: see DESIGN.md)
BOLT_TOOTH = (161.0, 127.0)       # one full tooth along a bolt
BOLT_STROKE = (260.3, -153.4)     # the shallow stroke of a tooth
BOLT_SWEEP = (-176.0, 210.0)      # step from one bolt to the next
BOLT_SHARE = 0.47                 # share of each repeat taken by the bolt
BOLT_PHASE = (0.417, 0.206)
BOLT_ORIGIN = (40.0, 120.0)
BOLT_ZOOM = 1.1                   # card px per pattern unit
FADE_START = 250                  # card px, at mid height, where the pattern starts to show
FADE_LENGTH = 640                 # card px to reach full strength
FADE_SLANT = 0.52
# The GunnerWired mark (white on transparent, PNG) so no extra image file is needed.
MARK_PNG = base64.b64decode(
    "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"
    "x2rv0v8HMxYe11AY8ekAAAAASUVORK5CYII="
)
_pil_cache = {}
_font_cache = {}


def _pil():
    """Return the Pillow modules, installing Pillow on the GitHub runner if needed."""
    if "mods" in _pil_cache:
        return _pil_cache["mods"]
    mods = None
    try:
        from PIL import Image, ImageDraw, ImageFont

        mods = (Image, ImageDraw, ImageFont)
    except ImportError:
        if os.environ.get("GITHUB_ACTIONS") == "true":
            base = [sys.executable, "-m", "pip", "install", "--quiet", "--user", "pillow"]
            for cmd in (base + ["--break-system-packages"], base):
                try:
                    if subprocess.run(cmd, timeout=180).returncode == 0:
                        break
                except Exception:
                    pass
            try:
                import importlib
                import site

                user_site = site.getusersitepackages()
                if user_site not in sys.path:
                    sys.path.append(user_site)
                importlib.invalidate_caches()
                from PIL import Image, ImageDraw, ImageFont

                mods = (Image, ImageDraw, ImageFont)
            except Exception as e:
                log(f"warning: Pillow is not available, posting text only: {e}")
    _pil_cache["mods"] = mods
    return mods


def _px(value):
    return int(round(value * CARD_SS))


def _font(kind, size):
    """kind: 'display' (League Gothic) or 'small' (Poppins Medium). size in drawn px."""
    key = (kind, int(round(size)))
    if key not in _font_cache:
        _, _, ImageFont = _pil()
        here = os.path.dirname(os.path.abspath(__file__))
        wanted = CARD_FONT_DISPLAY if kind == "display" else CARD_FONT_SMALL
        for path in (
            os.path.join(here, wanted),
            os.path.join(here, "fonts", wanted),
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        ):
            if os.path.exists(path):
                _font_cache[key] = ImageFont.truetype(path, key[1])
                break
        else:
            _font_cache[key] = ImageFont.load_default(key[1])
    return _font_cache[key]


def _bolt_mask(width, height):
    """White bolts on black, covering width x height drawn px."""
    Image, ImageDraw, _ = _pil()
    scale = BOLT_ZOOM * CARD_SS
    v1x, v1y = BOLT_TOOTH
    wx, wy = BOLT_SWEEP
    det = v1x * wy - wx * v1y

    def to_lattice(x, y):
        return (x * wy - wx * y) / det, (v1x * y - v1y * x) / det

    def to_px(s, r):
        ux, uy = s * v1x + r * wx, s * v1y + r * wy
        return (ux - BOLT_ORIGIN[0]) * scale, (uy - BOLT_ORIGIN[1]) * scale

    sa, ra = to_lattice(*BOLT_STROKE)
    s0, r0 = BOLT_PHASE
    corners = [
        to_lattice(x / scale + BOLT_ORIGIN[0], y / scale + BOLT_ORIGIN[1])
        for x, y in ((0, 0), (width, 0), (0, height), (width, height))
    ]
    s_lo = int(min(c[0] for c in corners)) - 3
    s_hi = int(max(c[0] for c in corners)) + 3
    r_lo = int(min(c[1] for c in corners)) - 3
    r_hi = int(max(c[1] for c in corners)) + 3
    mask = Image.new("L", (width, height), 0)
    d = ImageDraw.Draw(mask)
    for k in range(r_lo, r_hi + 1):
        lower = []
        for n in range(s_lo, s_hi + 1):
            lower.append((s0 + n, r0 + k))
            lower.append((s0 + n + sa, r0 + k + ra))
        upper = [(s, r + BOLT_SHARE) for s, r in reversed(lower)]
        d.polygon([to_px(s, r) for s, r in lower + upper], fill=255)
    return mask


def _fade_mask(width, height):
    """0 on the left (solid colour) rising to 255 (full pattern), along the bolts' slant."""
    Image, _, _ = _pil()
    span = int(width + FADE_SLANT * height) + 4
    start = (FADE_START + FADE_SLANT * CARD_H / 2) * CARD_SS
    length = FADE_LENGTH * CARD_SS
    values = []
    for i in range(span):
        t = min(1.0, max(0.0, (i - start) / length))
        values.append(int(round(255 * t * t * (3 - 2 * t))))
    ramp = Image.new("L", (span, 1))
    ramp.putdata(values)
    return ramp.transform((width, height), Image.AFFINE, (1, FADE_SLANT, 0, 0, 0, 0), resample=Image.BILINEAR)


def _card_background(style):
    Image, _, _ = _pil()
    from PIL import ImageChops

    size = (_px(CARD_W), _px(CARD_H))
    mask = ImageChops.multiply(_bolt_mask(*size), _fade_mask(*size))
    return Image.composite(Image.new("RGB", size, style["bolt"]), Image.new("RGB", size, style["bg"]), mask)


def _tracked(d, x, y, text, font, fill, track):
    """Letter-spaced text, left aligned, sitting on the baseline y. x, y, track in card px."""
    cx = _px(x)
    for ch in text:
        d.text((cx, _px(y)), ch, font=font, fill=fill, anchor="ls")
        cx += d.textlength(ch, font=font) + _px(track)


def _text_width(d, text, kind, size, track):
    """Width in card px of letter-spaced text at a size given in card px."""
    return d.textlength(text, font=_font(kind, _px(size))) / CARD_SS + track * (len(text) - 1)


def _fit(d, text, kind, max_width, start, smallest, track=0):
    size = start
    while size > smallest and _text_width(d, text, kind, size, track) > max_width:
        size -= 2
    return size


def _title_strip(text, size, track):
    """The title drawn horizontally, cropped to its ink, with the bottom cut exactly on
    the baseline so flat-bottomed letters reach the card edge."""
    Image, ImageDraw, _ = _pil()
    font = _font("display", _px(size))
    tmp = Image.new("RGBA", (_px(size * len(text)), _px(size * 1.6)), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    cx = _px(size * 0.5)
    for ch in text:
        td.text((cx, tmp.height / 2), ch, font=font, fill=CARD_TEXT, anchor="lm")
        cx += td.textlength(ch, font=font) + _px(track)
    left, top, right, _ = tmp.getbbox()
    flat = Image.new("L", (_px(size), tmp.height), 0)
    ImageDraw.Draw(flat).text((_px(size * 0.2), tmp.height / 2), "H", font=font, fill=255, anchor="lm")
    baseline = flat.point(lambda v: 255 if v > 200 else 0).getbbox()[3]
    return tmp.crop((left, top, right, baseline))


def _full_height_title(img, text, track=4):
    """Vertical title on the right edge, touching the top, bottom and right. Returns its left edge (card px)."""
    Image, _, _ = _pil()
    bleed = 4
    target = _px(CARD_H) + 2 * bleed
    size = 300.0
    for _ in range(4):
        size *= target / _title_strip(text, size, track).width
    strip = _title_strip(text, size, track)
    strip = strip.resize((target, round(strip.height * target / strip.width)), Image.LANCZOS)
    rot = strip.rotate(90, expand=True)
    x = _px(CARD_W) - rot.width + bleed
    img.paste(rot, (x, -bleed), rot)
    return x / CARD_SS


def _card_base(match, title):
    Image, ImageDraw, _ = _pil()
    style = CARD_STYLES["home" if is_home(match) else "away"]
    img = _card_background(style)
    left = _full_height_title(img, title)
    d = ImageDraw.Draw(img)
    mark = Image.open(io.BytesIO(MARK_PNG)).convert("RGBA")
    mark = mark.resize((_px(120), round(_px(120) * mark.height / mark.width)), Image.LANCZOS)
    tint = Image.new("RGBA", mark.size, CARD_ACCENT + (255,))
    tint.putalpha(mark.getchannel("A"))
    img.paste(tint, (_px(64), _px(96) - mark.height // 2), tint)
    _tracked(d, 204, 105, "GUNNERWIRED", _font("small", _px(20)), CARD_TEXT, 6)
    return img, d, left


def _card_footer(d, left, lines):
    room = left - 64 - 40
    d.line([(_px(64), _px(1086)), (_px(min(640, left - 40)), _px(1086))], fill=CARD_ACCENT, width=_px(2))
    y = 1134
    for line in lines:
        text = line.upper()
        size = _fit(d, text, "small", room, 19, 12, 6)
        _tracked(d, 64, y, text, _font("small", _px(size)), CARD_TEXT, 6)
        y += 40
    link = ("t.me/" + CHANNEL.lstrip("@")).upper()
    _tracked(d, 64, 1262, link, _font("small", _px(21)), CARD_ACCENT, 6)


def _card_bytes(img):
    Image, _, _ = _pil()
    out = io.BytesIO()
    img.resize((CARD_W, CARD_H), Image.LANCZOS).save(out, format="PNG")
    return out.getvalue()


def wrap(d, text, size, width):
    words, lines, line = text.upper().split(), [], ""
    for w in words:
        trial = (line + " " + w).strip()
        if _text_width(d, trial, "display", size, 2) <= width or not line:
            line = trial
        else:
            lines.append(line)
            line = w
    lines.append(line)
    return lines


TITLES = ["LATEST NEWS", "TEAM NEWS", "TRANSFER NEWS", "INJURY NEWS", "MATCH PREVIEW", "MATCH REPORT",
          "STAT ATTACK", "ON THIS DAY", "THE BIG QUESTION", "ACADEMY NEWS", "WOMEN'S TEAM"]


def news_card(title, kicker, headline, sub, style):
    if title.upper() not in TITLES:
        raise SystemExit(f"title must be one of: {', '.join(TITLES)}")
    if _pil() is None:
        raise SystemExit("Pillow is not available")
    fake = {"homeTeam": {"id": TEAM_ID if style == "home" else 0}}
    img, d, left = _card_base(fake, title.upper())
    room = left - 64 - 40
    _tracked(d, 64, 300, kicker.upper(), _font("small", _px(19)), CARD_ACCENT, 6)
    size = 150
    while size > 60:
        lines = wrap(d, headline, size, room)
        if len(lines) * size * 0.92 <= 640 and all(_text_width(d, l, "display", size, 2) <= room for l in lines):
            break
        size -= 4
    y = 300 + 40 + size * 0.86
    for line in lines:
        _tracked(d, 64, y, line, _font("display", _px(size)), CARD_TEXT, 2)
        y += size * 0.92
    _card_footer(d, left, [sub] if sub else [])
    return _card_bytes(img)


if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--title", default="LATEST NEWS")
    a.add_argument("--kicker", default="ARSENAL")
    a.add_argument("--headline", required=True)
    a.add_argument("--sub", default="")
    a.add_argument("--style", choices=["home", "away"], default="home")
    a.add_argument("--out", required=True)
    o = a.parse_args()
    with open(o.out, "wb") as f:
        f.write(news_card(o.title, o.kicker, o.headline, o.sub, o.style))
    print("saved", o.out)
