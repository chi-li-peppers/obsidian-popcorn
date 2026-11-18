"""Build theme.css for Popcorn.

Each palette is defined by a dark base color and two accents. Everything else
(light mode, text colors, folder colors, contrast-safe accents) is derived here.
Run:  python3 src/gen.py
"""
import colorsys
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")

# slug, name, inspired by, dark base, accent A, accent B
PALETTES = [
    ("arrakis", "Arrakis", "Dune", "#1a120b", "#e8a24a", "#c9733a"),
    ("upside-down", "Upside Down", "Stranger Things", "#0a0d1a", "#e5484d", "#4a6cff"),
    ("digital-rain", "Digital Rain", "The Matrix", "#020a04", "#39ff6a", "#0fa24a"),
    ("off-world", "Off-World", "Blade Runner 2049", "#160a04", "#ff8a2a", "#ff3d7f"),
    ("macrodata", "Macrodata", "Severance", "#0a1416", "#5fd3c8", "#9ab8b3"),
    ("black-lodge", "Black Lodge", "Twin Peaks", "#140405", "#e0353a", "#e8e2d6"),
    ("night-drive", "Night Drive", "Drive", "#0b0a18", "#ff7ac6", "#7b8cff"),
    ("gargantua", "Gargantua", "Interstellar", "#07070a", "#f2b84b", "#ff8c42"),
    ("trinity", "Trinity", "Oppenheimer", "#120a06", "#ff6a2a", "#ffc15e"),
    ("wasteland", "Wasteland", "Mad Max: Fury Road", "#150c08", "#ff7b2e", "#2fb8c4"),
    ("cordyceps", "Cordyceps", "The Last of Us", "#0c120c", "#8bbf5a", "#e0a458"),
    ("the-down-deep", "The Down Deep", "Silo", "#0f0f0d", "#f2c230", "#8f9a8a"),
    ("terminus", "Terminus", "Foundation", "#08091a", "#d8b45a", "#6aa6ff"),
    ("redwood", "Redwood", "Sons of Anarchy", "#120c0b", "#d63a30", "#b8b8b8"),
    ("dragonstone", "Dragonstone", "House of the Dragon", "#0c0a0a", "#e2452f", "#c9962e"),
    ("nine-nine", "Nine-Nine", "Brooklyn Nine-Nine", "#0a1020", "#4f86ff", "#ffd23f"),
    ("rolling-stone", "Rolling Stone", "Reacher", "#12110f", "#c9a46a", "#7f93a3"),
    ("grand-pastel", "Grand Pastel", "The Grand Budapest Hotel", "#1a1218", "#f19bb6", "#b9a2e6"),
    ("plastic-pink", "Plastic Pink", "Barbie", "#1a0a14", "#ff3fa4", "#ff9ad5"),
    ("nevermore", "Nevermore", "Wednesday", "#0a0a0b", "#a98be0", "#e6e6e6"),
    ("glitter", "Glitter", "Euphoria", "#120a1e", "#b45cff", "#4de3ff"),
    ("yes-chef", "Yes Chef", "The Bear", "#0d1216", "#4a90d9", "#c8cfd6"),
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
    return 0.2126 * c(r) + 0.7152 * c(g) + 0.0722 * c(b)


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


def build(slug, name, film, base, a, b):
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
    )
    for p in (dark, light):
        p["on_a"] = "#ffffff" if contrast("#ffffff", p["a"]) >= contrast("#111111", p["a"]) else "#111111"
        # six folder / canvas colors: the two accents, their mix, and three hue steps from A
        h0, l0, s0 = hls(p["a"])
        cs = [p["a"], p["b"], mix(p["a"], p["b"], 0.5)]
        for step in (0.33, 0.5, 0.75):
            cs.append(fit(mk(h0 + step, l0, max(s0, 0.45)), p["eff"], 3.0))
        p["c"] = cs
    out["dark"], out["light"] = dark, light
    return out


def block(selector, p, include_surfaces):
    lines = [
        f"--pc-a: {p['a']};", f"--pc-b: {p['b']};",
        f"--pc-a-rgb: {triplet(p['a'])};", f"--pc-b-rgb: {triplet(p['b'])};",
        f"--pc-glow-a-rgb: {triplet(p['glow_a'])};", f"--pc-glow-b-rgb: {triplet(p['glow_b'])};",
        f"--pc-text: {p['text']};", f"--pc-text-rgb: {triplet(p['text'])};",
        f"--pc-muted: {p['muted']};", f"--pc-faint: {p['faint']};",
        f"--pc-on-a: {p['on_a']};",
    ]
    h, l, s = hls(p["a"])
    lines.append(f"--accent-h: {round(h * 360)}; --accent-s: {round(s * 100)}%; --accent-l: {round(l * 100)}%;")
    for i, c in enumerate(p["c"], 1):
        lines.append(f"--pc-c{i}: {c}; --pc-c{i}-rgb: {triplet(c)};")
    if include_surfaces:
        lines += [f"--pc-bg: {p['bg']};", f"--pc-panel-rgb: {triplet(p['panel'])};", f"--pc-panel: {p['panel']};"]
    return selector + " {\n  " + "\n  ".join(lines) + "\n}\n"


def main():
    data = {s: build(s, n, f, base, a, b) for s, n, f, base, a, b in PALETTES}

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
    open(os.path.join(ROOT, "theme.css"), "w").write("".join(css))

    # palette data for the preview page and docs
    meta = [dict(slug=s, name=n, film=f, dark=data[s]["dark"], light=data[s]["light"]) for s, n, f, *_ in PALETTES]
    json.dump(meta, open(os.path.join(HERE, "palettes.json"), "w"), indent=1)
    print(f"theme.css written: {len(PALETTES)} palettes")


if __name__ == "__main__":
    main()
