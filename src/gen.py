"""Build theme.css for Popcorn.

Each palette has a color grade AND its own film-inspired visual language:
typography, geometry (border radius), border treatment, glow, and signature CSS.
Run:  python3 src/gen.py
"""
import colorsys
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")

# Font stacks (zero external downloads — crisp native fonts on macOS, iOS, Windows, Linux)
SANS = 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
SERIF = '"Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif'
MONO = '"SF Mono", ui-monospace, "JetBrains Mono", Menlo, Consolas, monospace'
ROUND = '"SF Pro Rounded", "Avenir Next", -apple-system, BlinkMacSystemFont, sans-serif'

# slug, name, inspired by, dark base, accent A, accent B, style dict
PALETTES = [
    ("arrakis", "Arrakis", "Dune", "#1a120b", "#e8a24a", "#c9733a", dict(
        body=SANS, head=SERIF, radius="14px", card_r="10px", head_ls="0.04em", head_tt="uppercase",
        h1_scale="1.06", glass="0.68",
    )),
    ("upside-down", "Upside Down", "Stranger Things", "#090b16", "#ef3e4a", "#4a6cff", dict(
        body=SANS, head=SERIF, radius="10px", card_r="8px", head_ls="0.03em", head_tt="uppercase",
        h1_scale="1.08", glass="0.62",
    )),
    ("digital-rain", "Digital Rain", "The Matrix", "#020904", "#39ff6a", "#0fa24a", dict(
        body=MONO, head=MONO, radius="4px", card_r="3px", head_ls="0.04em", head_tt="uppercase",
        h1_scale="0.96", glass="0.72",
    )),
    ("off-world", "Off-World", "Blade Runner 2049", "#140905", "#ff8a2a", "#ff3d7f", dict(
        body=SANS, head=SANS, radius="6px", card_r="5px", head_ls="0.06em", head_tt="uppercase",
        h1_scale="1.0", glass="0.60",
    )),
    ("macrodata", "Macrodata", "Severance", "#091315", "#5fd3c8", "#9ab8b3", dict(
        body=SANS, head=MONO, radius="4px", card_r="4px", head_ls="0.06em", head_tt="uppercase",
        h1_scale="0.96", glass="0.76",
    )),
    ("black-lodge", "Black Lodge", "Twin Peaks", "#140405", "#e0353a", "#e8e2d6", dict(
        body=SERIF, head=SERIF, radius="8px", card_r="6px", head_ls="0.02em", head_tt="none",
        h1_scale="1.06", glass="0.68",
    )),
    ("night-drive", "Night Drive", "Drive", "#0b0918", "#ff6ac1", "#7b8cff", dict(
        body=SANS, head=SANS, radius="16px", card_r="12px", head_ls="-0.02em", head_tt="none",
        h1_scale="1.04", glass="0.58",
    )),
    ("gargantua", "Gargantua", "Interstellar", "#050508", "#f2b84b", "#ff8c42", dict(
        body=SANS, head=SANS, radius="18px", card_r="14px", head_ls="0.08em", head_tt="uppercase",
        h1_scale="1.02", glass="0.56",
    )),
    ("trinity", "Trinity", "Oppenheimer", "#110a06", "#ff6a2a", "#ffc15e", dict(
        body=SERIF, head=SERIF, radius="6px", card_r="4px", head_ls="0.01em", head_tt="none",
        h1_scale="1.08", glass="0.74",
    )),
    ("wasteland", "Wasteland", "Mad Max: Fury Road", "#150c07", "#ff7b2e", "#2fb8c4", dict(
        body=SANS, head=SANS, radius="4px", card_r="4px", head_ls="0.05em", head_tt="uppercase",
        h1_scale="1.05", glass="0.70",
    )),
    ("cordyceps", "Cordyceps", "The Last of Us", "#0b110b", "#8bbf5a", "#e0a458", dict(
        body=SANS, head=SERIF, radius="14px", card_r="12px", head_ls="-0.01em", head_tt="none",
        h1_scale="1.04", glass="0.68",
    )),
    ("the-down-deep", "The Down Deep", "Silo", "#0e0f0d", "#f2c230", "#8f9a8a", dict(
        body=SANS, head=MONO, radius="4px", card_r="3px", head_ls="0.05em", head_tt="uppercase",
        h1_scale="0.98", glass="0.76",
    )),
    ("terminus", "Terminus", "Foundation", "#07091a", "#d8b45a", "#6aa6ff", dict(
        body=SANS, head=SERIF, radius="14px", card_r="10px", head_ls="0.04em", head_tt="none",
        h1_scale="1.06", glass="0.62",
    )),
    ("redwood", "Redwood", "Sons of Anarchy", "#110b0a", "#d63a30", "#b8b8b8", dict(
        body=SANS, head=SANS, radius="4px", card_r="4px", head_ls="0.04em", head_tt="uppercase",
        h1_scale="1.04", glass="0.76",
    )),
    ("dragonstone", "Dragonstone", "House of the Dragon", "#0c0909", "#e2452f", "#c9962e", dict(
        body=SERIF, head=SERIF, radius="8px", card_r="6px", head_ls="0.03em", head_tt="uppercase",
        h1_scale="1.05", glass="0.70",
    )),
    ("nine-nine", "Nine-Nine", "Brooklyn Nine-Nine", "#0a1020", "#4f86ff", "#ffd23f", dict(
        body=SANS, head=ROUND, radius="14px", card_r="12px", head_ls="-0.01em", head_tt="none",
        h1_scale="1.02", glass="0.64",
    )),
    ("rolling-stone", "Rolling Stone", "Reacher", "#11100e", "#c9a46a", "#7f93a3", dict(
        body=SANS, head=SANS, radius="6px", card_r="6px", head_ls="0.02em", head_tt="none",
        h1_scale="1.02", glass="0.76",
    )),
    ("grand-pastel", "Grand Pastel", "The Grand Budapest Hotel", "#1a1218", "#f19bb6", "#b9a2e6", dict(
        body=SERIF, head=SERIF, radius="12px", card_r="8px", head_ls="0.05em", head_tt="uppercase",
        h1_scale="1.04", glass="0.72",
    )),
    ("plastic-pink", "Plastic Pink", "Barbie", "#1a0a14", "#ff3fa4", "#ff9ad5", dict(
        body=ROUND, head=ROUND, radius="24px", card_r="20px", head_ls="-0.01em", head_tt="none",
        h1_scale="1.06", glass="0.66",
    )),
    ("nevermore", "Nevermore", "Wednesday", "#09090b", "#a98be0", "#e6e6e6", dict(
        body=SERIF, head=SERIF, radius="6px", card_r="4px", head_ls="0.03em", head_tt="none",
        h1_scale="1.06", glass="0.72",
    )),
    ("glitter", "Glitter", "Euphoria", "#11091e", "#b45cff", "#4de3ff", dict(
        body=SANS, head=ROUND, radius="22px", card_r="18px", head_ls="-0.02em", head_tt="none",
        h1_scale="1.04", glass="0.54",
    )),
    ("yes-chef", "Yes Chef", "The Bear", "#0c1116", "#4a90d9", "#c8cfd6", dict(
        body=SANS, head=MONO, radius="6px", card_r="4px", head_ls="0.04em", head_tt="uppercase",
        h1_scale="0.98", glass="0.74",
    )),
]
DEFAULT = "arrakis"


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def hexs(r, g, b):
    return "#%02x%02x%02x" % tuple(round(max(0, min(1, v)) * 255) for v in (r, g, b))


def hls(h):
    return colorsys.rgb_to_hls(*rgb(h))


def mk(h, l, s):
    return hexs(*colorsys.hls_to_rgb(h % 1, max(0, min(1, l)), max(0, min(1, s))))


def mix(a, b, t):
    ra, rb = rgb(a), rgb(b)
    return hexs(*(x * (1 - t) + y * t for x, y in zip(ra, rb)))


def lum(h):
    def c(v):
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = rgb(h)
    return 0.2126 * c(r) + 0.7152 * c(g) + 0.722 * 0 + 0.0722 * c(b)


def contrast(a, b):
    x, y = sorted([lum(a), lum(b)], reverse=True)
    return (x + 0.05) / (y + 0.05)


def fit(color, bg, target):
    """Move lightness away from the background until contrast reaches target."""
    h, l, s = hls(color)
    darker = lum(bg) > 0.4
    for _ in range(80):
        c = mk(h, l, s)
        if contrast(c, bg) >= target:
            return c
        l += -0.012 if darker else 0.012
    return mk(h, l, s)


def triplet(h):
    return ", ".join(str(round(v * 255)) for v in rgb(h))


def build(slug, name, film, base, a, b, style):
    bh, bl, bs = hls(base)
    ah, al, asat = hls(a)
    out = {}

    # dark
    panel_d = mk(bh, 0.13, min(bs, 0.55) * 0.6)
    eff_d = mix(panel_d, base, 0.35)
    text_d = mk(bh, 0.92, 0.12)
    dark = dict(
        bg=base, panel=panel_d, eff=eff_d,
        text=text_d, muted=mk(bh, 0.70, 0.10), faint=mk(bh, 0.50, 0.08),
        a=fit(a, eff_d, 4.5), b=fit(b, eff_d, 3.0),
        glow_a=a, glow_b=b,
        style=style,
    )
    # light
    bg_l = mk(ah, 0.935, min(asat, 0.8) * 0.45)
    panel_l = "#ffffff"
    eff_l = mix(panel_l, bg_l, 0.35)
    light = dict(
        bg=bg_l, panel=panel_l, eff=eff_l,
        text=mk(ah, 0.13, 0.25), muted=mk(ah, 0.38, 0.12), faint=mk(ah, 0.55, 0.08),
        a=fit(a, eff_l, 4.5), b=fit(b, eff_l, 3.0),
        glow_a=mix(a, "#ffffff", 0.15), glow_b=mix(b, "#ffffff", 0.15),
        style=style,
    )
    for p in (dark, light):
        p["on_a"] = "#ffffff" if contrast("#ffffff", p["a"]) >= contrast("#111111", p["a"]) else "#111111"
        h0, l0, s0 = hls(p["a"])
        cs = [p["a"], p["b"], mix(p["a"], p["b"], 0.5)]
        for step in (0.33, 0.5, 0.75):
            cs.append(fit(mk(h0 + step, l0, max(s0, 0.45)), p["eff"], 3.0))
        p["c"] = cs
    out["dark"], out["light"] = dark, light
    return out


def block(selector, p, include_surfaces):
    st = p["style"]
    lines = [
        f"--pc-a: {p['a']};", f"--pc-b: {p['b']};",
        f"--pc-a-rgb: {triplet(p['a'])};", f"--pc-b-rgb: {triplet(p['b'])};",
        f"--pc-glow-a-rgb: {triplet(p['glow_a'])};", f"--pc-glow-b-rgb: {triplet(p['glow_b'])};",
        f"--pc-text: {p['text']};", f"--pc-text-rgb: {triplet(p['text'])};",
        f"--pc-muted: {p['muted']};", f"--pc-faint: {p['faint']};",
        f"--pc-on-a: {p['on_a']};",
        f"--pc-font-body: {st['body']};",
        f"--pc-font-head: {st['head']};",
        f"--pc-head-ls: {st['head_ls']};",
        f"--pc-head-tt: {st['head_tt']};",
        f"--pc-card-radius: {st['card_r']};",
    ]
    h, l, s = hls(p["a"])
    lines.append(f"--accent-h: {round(h * 360)}; --accent-s: {round(s * 100)}%; --accent-l: {round(l * 100)}%;")
    for i, c in enumerate(p["c"], 1):
        lines.append(f"--pc-c{i}: {c}; --pc-c{i}-rgb: {triplet(c)};")
    if include_surfaces:
        lines += [
            f"--pc-bg: {p['bg']};",
            f"--pc-panel-rgb: {triplet(p['panel'])};",
            f"--pc-panel: {p['panel']};",
            f"--pc-radius: {st['radius']};",
            f"--pc-glass: {st['glass']};",
        ]
    return selector + " {\n  " + "\n  ".join(lines) + "\n}\n"


# Signature film-specific CSS flourishes (zero images, pure CSS, dark + light safe)
SIGNATURES = """
/* =====================================================================
   Film-specific visual signatures — distinct layouts, chrome & textures
   ===================================================================== */

/* ── 1. Digital Rain (The Matrix) — pure hacker terminal, 0px corners, CRT scanlines, phosphor glow ── */
body.popcorn-v-digital-rain {
  --pc-radius: 2px;
  --pc-card-radius: 0px;
  --tag-radius: 2px;
  --checkbox-radius: 1px;
  --nav-item-radius: 2px;
}
body.popcorn-v-digital-rain .workspace-split.mod-left-split,
body.popcorn-v-digital-rain .workspace-split.mod-right-split,
body.popcorn-v-digital-rain .workspace-split.mod-root {
  background:
    repeating-linear-gradient(0deg, rgba(var(--pc-a-rgb), 0.055) 0 1px, transparent 1px 4px),
    rgba(var(--pc-panel-rgb), 0.88);
  border: 1px solid rgba(var(--pc-a-rgb), 0.50);
  box-shadow: 0 0 24px rgba(var(--pc-a-rgb), 0.14), inset 0 0 24px rgba(var(--pc-a-rgb), 0.05);
}
body.popcorn-v-digital-rain .mod-root .workspace-tab-header { border-radius: 2px !important; }
body.popcorn-v-digital-rain .mod-root .workspace-tab-header.is-active {
  background: rgba(var(--pc-a-rgb), 0.18) !important;
  border: 1px solid var(--pc-a) !important;
  color: var(--pc-a) !important;
}
body.popcorn-v-digital-rain .inline-title::before { content: "> "; opacity: 0.65; }
body.popcorn-v-digital-rain .markdown-rendered h2::before { content: "$ "; opacity: 0.55; }
body.theme-dark.popcorn-v-digital-rain .inline-title,
body.theme-dark.popcorn-v-digital-rain .markdown-rendered h2,
body.theme-dark.popcorn-v-digital-rain .markdown-rendered h3 {
  color: var(--pc-a);
  text-shadow: 0 0 14px rgba(var(--pc-a-rgb), 0.60);
}
body.popcorn-v-digital-rain .callout {
  border: 1px solid rgba(var(--pc-a-rgb), 0.55);
  border-left: 4px solid var(--pc-a);
  background: rgba(var(--pc-a-rgb), 0.07);
}
body.popcorn-v-digital-rain .markdown-rendered .contains-task-list > .task-list-item {
  border: 1px solid rgba(var(--pc-a-rgb), 0.25);
  background: rgba(var(--pc-a-rgb), 0.04);
}
body.popcorn-v-digital-rain .status-bar { border-radius: 2px !important; border-color: rgba(var(--pc-a-rgb), 0.45) !important; }

/* ── 2. Grand Pastel (The Grand Budapest Hotel) — Wes Anderson symmetry, ornate double frames ── */
body.popcorn-v-grand-pastel {
  --pc-radius: 6px;
  --pc-card-radius: 4px;
  --tag-radius: 4px;
}
body.popcorn-v-grand-pastel .workspace-split.mod-root,
body.popcorn-v-grand-pastel .workspace-split.mod-left-split,
body.popcorn-v-grand-pastel .workspace-split.mod-right-split {
  border: 2px solid rgba(var(--pc-a-rgb), 0.55);
  box-shadow: 0 18px 48px rgba(40, 20, 40, 0.14), inset 0 0 0 4px transparent, inset 0 0 0 5px rgba(var(--pc-a-rgb), 0.28);
}
body.popcorn-v-grand-pastel .mod-root .workspace-tab-header { border-radius: 3px !important; text-transform: uppercase; letter-spacing: 0.08em; font-size: 11px; }
body.popcorn-v-grand-pastel .mod-root .workspace-tab-header.is-active {
  border: 1px solid rgba(var(--pc-a-rgb), 0.65) !important;
  background: rgba(var(--pc-a-rgb), 0.18) !important;
}
body.popcorn-v-grand-pastel .inline-title {
  text-align: center;
  border-top: 2px solid rgba(var(--pc-a-rgb), 0.60);
  border-bottom: 2px solid rgba(var(--pc-a-rgb), 0.60);
  padding: 10px 0;
  letter-spacing: 0.14em;
}
body.popcorn-v-grand-pastel .markdown-rendered h2 {
  text-align: center;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-size: 1.15em;
}
body.popcorn-v-grand-pastel .callout {
  border: 2px double rgba(var(--pc-a-rgb), 0.65);
  outline: 1px solid rgba(var(--pc-b-rgb), 0.45);
  outline-offset: -6px;
  padding: 16px 20px;
}
body.popcorn-v-grand-pastel .status-bar { border-radius: 4px !important; border: 1px solid rgba(var(--pc-a-rgb), 0.45) !important; }

/* ── 3. Upside Down (Stranger Things) — 80s horror neon crimson title, glowing red bars, red/blue fog ── */
body.popcorn-v-upside-down {
  --pc-radius: 6px;
  --pc-card-radius: 4px;
}
body.popcorn-v-upside-down .app-container {
  background:
    radial-gradient(75vw 65vh at 5% 0%, rgba(var(--pc-glow-a-rgb), 0.62), transparent 58%),
    radial-gradient(75vw 65vh at 98% 100%, rgba(var(--pc-glow-b-rgb), 0.58), transparent 60%),
    var(--pc-bg);
}
body.theme-dark.popcorn-v-upside-down .workspace-split.mod-root {
  border: 1px solid rgba(var(--pc-a-rgb), 0.45);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.55), 0 0 36px rgba(var(--pc-a-rgb), 0.18);
}
body.theme-dark.popcorn-v-upside-down .inline-title {
  color: #ff4552;
  text-shadow: 0 0 12px rgba(239, 62, 74, 0.90), 0 0 28px rgba(239, 62, 74, 0.55);
  border-top: 3px solid #ef3e4a;
  border-bottom: 3px solid #ef3e4a;
  box-shadow: 0 -2px 12px -4px rgba(239, 62, 74, 0.7), 0 2px 12px -4px rgba(239, 62, 74, 0.7);
  padding: 8px 4px;
  letter-spacing: 0.12em;
  display: inline-block;
}
body.popcorn-v-upside-down .callout {
  border: 1px solid rgba(var(--pc-a-rgb), 0.55);
  box-shadow: 0 0 20px rgba(var(--pc-a-rgb), 0.16);
}

/* ── 4. Macrodata (Severance) — Lumon clinical dot-grid INSIDE panels, flat underlined tabs, sterile boxes ── */
body.popcorn-v-macrodata {
  --pc-radius: 2px;
  --pc-card-radius: 2px;
  --tag-radius: 2px;
  --checkbox-radius: 2px;
  --nav-item-radius: 2px;
}
body.popcorn-v-macrodata .workspace-split.mod-root {
  background:
    radial-gradient(rgba(var(--pc-a-rgb), 0.13) 1px, transparent 1px) 0 0 / 20px 20px,
    rgba(var(--pc-panel-rgb), 0.86);
  border: 1.5px solid rgba(var(--pc-a-rgb), 0.42);
}
body.popcorn-v-macrodata .workspace-split.mod-left-split,
body.popcorn-v-macrodata .workspace-split.mod-right-split {
  border: 1.5px solid rgba(var(--pc-a-rgb), 0.32);
}
body.popcorn-v-macrodata .mod-root .workspace-tab-header {
  border-radius: 0 !important;
  border-bottom: 2px solid transparent !important;
  background: transparent !important;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 11px;
}
body.popcorn-v-macrodata .mod-root .workspace-tab-header.is-active {
  border: 0 !important;
  border-bottom: 2px solid var(--pc-a) !important;
  background: rgba(var(--pc-a-rgb), 0.10) !important;
  color: var(--pc-a) !important;
}
body.popcorn-v-macrodata .markdown-rendered h2 {
  display: inline-block;
  padding: 3px 10px;
  background: rgba(var(--pc-a-rgb), 0.14);
  border: 1px solid rgba(var(--pc-a-rgb), 0.40);
  color: var(--pc-a);
  font-size: 0.95em;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}
body.popcorn-v-macrodata .status-bar { border-radius: 2px !important; }

/* ── 5. Black Lodge (Twin Peaks) — red velvet curtain stripes on sidebar & chevron zig-zag accent ── */
body.popcorn-v-black-lodge {
  --pc-radius: 4px;
  --pc-card-radius: 4px;
}
body.popcorn-v-black-lodge .workspace-split.mod-left-split,
body.popcorn-v-black-lodge .workspace-split.mod-right-split {
  background:
    repeating-linear-gradient(90deg, rgba(var(--pc-glow-a-rgb), 0.14) 0 18px, rgba(0, 0, 0, 0.12) 18px 36px),
    rgba(var(--pc-panel-rgb), 0.85);
  border: 1px solid rgba(var(--pc-a-rgb), 0.42);
}
body.popcorn-v-black-lodge .callout {
  border: 1px solid rgba(var(--pc-a-rgb), 0.45);
  border-top: 6px solid transparent;
  border-image: repeating-linear-gradient(135deg, #e8e2d6 0 8px, #140405 8px 16px) 6 0 0 0;
  background: linear-gradient(180deg, rgba(var(--pc-a-rgb), 0.18), rgba(var(--pc-a-rgb), 0.06));
}
body.popcorn-v-black-lodge .inline-title {
  border-bottom: 4px solid transparent;
  border-image: repeating-linear-gradient(135deg, var(--pc-b) 0 6px, var(--pc-a) 6px 12px) 0 0 4 0;
  padding-bottom: 8px;
}

/* ── 6. Plastic Pink (Barbie) — glossy 26px bubble-round pop-art, candy gradient active pill ── */
body.popcorn-v-plastic-pink {
  --pc-radius: 26px;
  --pc-card-radius: 20px;
  --tag-radius: 999px;
  --checkbox-radius: 999px;
}
body.popcorn-v-plastic-pink .workspace-split.mod-root,
body.popcorn-v-plastic-pink .workspace-split.mod-left-split,
body.popcorn-v-plastic-pink .workspace-split.mod-right-split {
  border: 2px solid rgba(var(--pc-a-rgb), 0.48);
  box-shadow: 0 20px 50px rgba(255, 63, 164, 0.18), inset 0 2px 0 rgba(255, 255, 255, 0.85);
}
body.popcorn-v-plastic-pink .mod-root .workspace-tab-header.is-active {
  background: linear-gradient(135deg, var(--pc-a), var(--pc-b)) !important;
  color: #ffffff !important;
  border: 0 !important;
  box-shadow: 0 4px 14px rgba(var(--pc-a-rgb), 0.35) !important;
}
body.popcorn-v-plastic-pink .inline-title {
  color: var(--pc-a);
  letter-spacing: -0.02em;
}
body.popcorn-v-plastic-pink .callout {
  border: 2px solid rgba(var(--pc-a-rgb), 0.45);
  box-shadow: 0 8px 20px rgba(var(--pc-a-rgb), 0.12);
}

/* ── 7. Night Drive (Drive) — neon pink/indigo synthwave glow & sleek italic title ── */
body.theme-dark.popcorn-v-night-drive .inline-title {
  font-style: italic;
  color: #fff;
  text-shadow: 0 0 18px rgba(var(--pc-a-rgb), 0.75), 0 0 36px rgba(var(--pc-b-rgb), 0.45);
}
body.popcorn-v-night-drive .workspace-split.mod-root {
  border: 1px solid rgba(var(--pc-a-rgb), 0.40);
  box-shadow: 0 24px 70px rgba(0, 0, 0, 0.45), 0 0 36px rgba(var(--pc-a-rgb), 0.16), inset 0 1px 0 rgba(var(--pc-a-rgb), 0.40);
}
body.popcorn-v-night-drive .mod-root .workspace-tab-header.is-active {
  background: linear-gradient(135deg, rgba(var(--pc-a-rgb), 0.28), rgba(var(--pc-b-rgb), 0.24)) !important;
  border: 1px solid rgba(var(--pc-a-rgb), 0.55) !important;
  box-shadow: 0 0 14px rgba(var(--pc-a-rgb), 0.25) !important;
}
body.popcorn-v-night-drive .callout {
  border: 1px solid rgba(var(--pc-a-rgb), 0.45);
  box-shadow: 0 0 22px rgba(var(--pc-a-rgb), 0.15);
}

/* ── 8. Arrakis (Dune) — desert spice horizon & carved architectural typography ── */
body.popcorn-v-arrakis {
  --pc-radius: 8px;
  --pc-card-radius: 6px;
}
body.popcorn-v-arrakis .app-container {
  background:
    radial-gradient(100vw 40vh at 50% -8%, rgba(var(--pc-glow-a-rgb), 0.62), transparent 65%),
    radial-gradient(70vw 50vh at 85% 105%, rgba(var(--pc-glow-b-rgb), 0.42), transparent 65%),
    var(--pc-bg);
}
body.popcorn-v-arrakis .inline-title {
  letter-spacing: 0.12em;
  border-bottom: 1.5px solid rgba(var(--pc-a-rgb), 0.55);
  padding-bottom: 8px;
}
body.popcorn-v-arrakis .callout {
  border-left: 3px solid var(--pc-a);
}

/* ── 9. The Down Deep (Silo) — industrial bunker blueprint grid & hazard-yellow caution stripes ── */
body.popcorn-v-the-down-deep {
  --pc-radius: 2px;
  --pc-card-radius: 2px;
  --tag-radius: 2px;
}
body.popcorn-v-the-down-deep .workspace-split.mod-root {
  background:
    linear-gradient(rgba(var(--pc-text-rgb), 0.035) 1px, transparent 1px) 0 0 / 26px 26px,
    linear-gradient(90deg, rgba(var(--pc-text-rgb), 0.035) 1px, transparent 1px) 0 0 / 26px 26px,
    rgba(var(--pc-panel-rgb), 0.88);
  border: 1.5px solid rgba(var(--pc-a-rgb), 0.35);
}
body.popcorn-v-the-down-deep .callout {
  border-left: 5px solid var(--pc-a);
  border-top: 4px solid transparent;
  border-image: repeating-linear-gradient(-45deg, var(--pc-a) 0 8px, #161714 8px 16px) 4 0 0 0;
}
body.popcorn-v-the-down-deep .markdown-rendered .contains-task-list > .task-list-item {
  border-left: 3px solid var(--pc-a);
}

/* ── 10. Yes Chef (The Bear) — Chicago kitchen order-ticket cards & dashed dividers ── */
body.popcorn-v-yes-chef {
  --pc-radius: 4px;
  --pc-card-radius: 3px;
}
body.popcorn-v-yes-chef .markdown-rendered .contains-task-list > .task-list-item {
  border: 1px dashed rgba(var(--pc-text-rgb), 0.22);
  border-left: 4px solid var(--pc-a);
}
body.popcorn-v-yes-chef .callout {
  border: 1px dashed rgba(var(--pc-a-rgb), 0.55);
  border-left: 4px solid var(--pc-a);
}
body.popcorn-v-yes-chef .markdown-rendered h2 {
  border-bottom: 1.5px dashed rgba(var(--pc-a-rgb), 0.50);
  padding-bottom: 4px;
}

/* ── 11. Off-World (Blade Runner 2049) — dystopian smog + cyberpunk HUD left bars ── */
body.popcorn-v-off-world {
  --pc-radius: 4px;
  --pc-card-radius: 3px;
}
body.popcorn-v-off-world .app-container {
  background:
    radial-gradient(85vw 60vh at 10% 0%, rgba(var(--pc-glow-a-rgb), 0.65), transparent 60%),
    radial-gradient(75vw 65vh at 95% 100%, rgba(var(--pc-glow-b-rgb), 0.55), transparent 58%),
    var(--pc-bg);
}
body.popcorn-v-off-world .callout,
body.popcorn-v-off-world .markdown-rendered .contains-task-list > .task-list-item {
  border-left: 3px solid var(--pc-a);
}
body.theme-dark.popcorn-v-off-world .inline-title {
  color: var(--pc-a);
  letter-spacing: 0.10em;
  text-shadow: 0 0 22px rgba(var(--pc-a-rgb), 0.50);
}

/* ── 12. Gargantua (Interstellar) — deep black cosmos & golden event-horizon arc ── */
body.popcorn-v-gargantua .app-container {
  background:
    radial-gradient(120vw 32vh at 50% -10%, rgba(var(--pc-glow-a-rgb), 0.58), transparent 64%),
    radial-gradient(95vw 24vh at 50% 110%, rgba(var(--pc-glow-b-rgb), 0.42), transparent 64%),
    #030306;
}
body.popcorn-v-gargantua .inline-title { letter-spacing: 0.16em; }
body.popcorn-v-gargantua .workspace-split.mod-root {
  border-color: rgba(var(--pc-a-rgb), 0.28);
  box-shadow: 0 24px 80px rgba(0, 0, 0, 0.7), inset 0 1px 0 rgba(var(--pc-a-rgb), 0.35);
}

/* ── 13. Glitter (Euphoria) — iridescent purple/cyan dreamy ultra-glass ── */
body.popcorn-v-glitter {
  --pc-radius: 24px;
  --pc-card-radius: 18px;
}
body.popcorn-v-glitter .app-container {
  background:
    radial-gradient(70vw 60vh at 8% 8%, rgba(var(--pc-glow-a-rgb), 0.65), transparent 58%),
    radial-gradient(70vw 60vh at 92% 92%, rgba(var(--pc-glow-b-rgb), 0.58), transparent 58%),
    var(--pc-bg);
}
body.popcorn-v-glitter .workspace-split.mod-root {
  border: 1.5px solid rgba(var(--pc-b-rgb), 0.42);
  box-shadow: 0 24px 70px rgba(0, 0, 0, 0.35), 0 0 40px rgba(var(--pc-a-rgb), 0.22), inset 0 1px 0 rgba(255, 255, 255, 0.24);
}
body.popcorn-v-glitter .mod-root .workspace-tab-header.is-active {
  background: linear-gradient(135deg, rgba(var(--pc-a-rgb), 0.35), rgba(var(--pc-b-rgb), 0.30)) !important;
  border: 1px solid rgba(var(--pc-b-rgb), 0.55) !important;
}

/* ── 14. Nevermore (Wednesday) — dark gothic academia double-rules ── */
body.popcorn-v-nevermore {
  --pc-radius: 4px;
  --pc-card-radius: 3px;
}
body.popcorn-v-nevermore .inline-title {
  border-bottom: 3px double rgba(var(--pc-text-rgb), 0.45);
  padding-bottom: 6px;
}
body.popcorn-v-nevermore .callout {
  border: 1px solid rgba(var(--pc-text-rgb), 0.22);
  border-left: 4px solid var(--pc-a);
  outline: 1px solid rgba(var(--pc-a-rgb), 0.22);
  outline-offset: -5px;
}

/* ── 15. Wasteland, Redwood, Trinity, Dragonstone, Terminus ── */
body.popcorn-v-wasteland .callout,
body.popcorn-v-redwood .callout {
  border-left: 4px solid var(--pc-a);
}
body.popcorn-v-wasteland .workspace-split.mod-root,
body.popcorn-v-redwood .workspace-split.mod-root {
  border: 1.5px solid rgba(var(--pc-a-rgb), 0.36);
}
body.popcorn-v-trinity .inline-title,
body.popcorn-v-dragonstone .inline-title,
body.popcorn-v-terminus .inline-title {
  border-bottom: 1.5px solid rgba(var(--pc-a-rgb), 0.48);
  padding-bottom: 6px;
}
"""


def main():
    data = {s: build(s, n, f, base, a, b, st) for s, n, f, base, a, b, st in PALETTES}

    opts = "\n".join(
        f"            -\n                label: \"{n} — {f}\"\n                value: popcorn-v-{s}"
        for s, n, f, *_ in PALETTES
    )
    settings = open(os.path.join(HERE, "settings.yml")).read().replace("{{OPTIONS}}", opts)

    css = ["/* Popcorn for Obsidian — glass theme with film and TV inspired palettes. MIT license.\n"
           "   theme.css is generated by src/gen.py from src/base.css and src/settings.yml. */\n\n",
           settings, "\n"]

    # global palette: default, then one per variant
    d = data[DEFAULT]
    css.append(block("body.theme-dark", d["dark"], True))
    css.append(block("body.theme-light", d["light"], True))
    for s, *_ in PALETTES:
        css.append(block(f"body.theme-dark.popcorn-v-{s}", data[s]["dark"], True))
        css.append(block(f"body.theme-light.popcorn-v-{s}", data[s]["light"], True))

    # per-note palettes via cssclasses: pc-<slug>
    for s, *_ in PALETTES:
        sel = lambda mode: ", ".join(
            f".theme-{mode} .{v}.pc-{s}" for v in ("markdown-preview-view", "markdown-source-view")
        )
        css.append(block(sel("dark"), data[s]["dark"], False))
        css.append(block(sel("light"), data[s]["light"], False))

    css.append(open(os.path.join(HERE, "base.css")).read())
    css.append(SIGNATURES)
    open(os.path.join(ROOT, "theme.css"), "w").write("".join(css))

    meta = [dict(slug=s, name=n, film=f, dark=data[s]["dark"], light=data[s]["light"]) for s, n, f, *_ in PALETTES]
    json.dump(meta, open(os.path.join(HERE, "palettes.json"), "w"), indent=1)
    print(f"theme.css written: {len(PALETTES)} palettes with film signatures")


if __name__ == "__main__":
    main()
