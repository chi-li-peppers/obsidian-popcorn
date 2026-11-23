#!/bin/zsh
# Regenerates theme.css and renders all README previews, all-scenes sheet, and screenshot.png.
set -e
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/docs/previews"
TMP="/tmp/pc-shots"
mkdir -p "$TMP" "$OUT"

python3 "$ROOT/src/gen.py"

shot_jpg() {  # out_name scene mode [size] [extra_qs]
  local name="$1" scene="$2" mode="$3" size="${4:-1440,900}" extra="$5"
  local qs="scene=${scene}&mode=${mode}"
  [[ -n "$extra" ]] && qs="${qs}&${extra}"
  "$CH" --headless=new --disable-gpu --hide-scrollbars --virtual-time-budget=2000 \
    --window-size="$size" --screenshot="$TMP/${name}.png" \
    "file://$ROOT/docs/preview.html?${qs}" >/dev/null 2>&1
  sips -s format jpeg -s formatOptions 90 "$TMP/${name}.png" --out "$OUT/${name}.jpg" >/dev/null 2>&1
}

# All 22 desktop palettes (Grand Pastel and Plastic Pink showcased in light mode)
DARK_SCENES=(
  arrakis upside-down digital-rain off-world macrodata black-lodge
  night-drive gargantua trinity wasteland cordyceps the-down-deep
  terminus redwood dragonstone nine-nine rolling-stone
  nevermore glitter yes-chef
)
LIGHT_SCENES=(grand-pastel plastic-pink)

for s in $DARK_SCENES; do
  shot_jpg "$s" "$s" dark 1440,900
done
for s in $LIGHT_SCENES; do
  shot_jpg "$s" "$s" light 1440,900
done

# Mobile previews
shot_jpg mobile-arrakis arrakis dark 390,844 "mobile=1"
shot_jpg mobile-night-drive night-drive dark 390,844 "mobile=1"
shot_jpg mobile-digital-rain digital-rain dark 390,844 "mobile=1"
shot_jpg mobile-grand-pastel grand-pastel light 390,844 "mobile=1"

# Obsidian Community Theme Store thumbnail (root screenshot.png)
"$CH" --headless=new --disable-gpu --hide-scrollbars --virtual-time-budget=2000 \
  --window-size=1280,800 --screenshot="$ROOT/screenshot.png" \
  "file://$ROOT/docs/preview.html?scene=night-drive&mode=dark" >/dev/null 2>&1

# Contact sheet of all 22 palettes
"$CH" --headless=new --disable-gpu --hide-scrollbars --virtual-time-budget=2500 \
  --window-size=1600,1740 --screenshot="$TMP/all-scenes.png" \
  "file://$ROOT/docs/sheet.html" >/dev/null 2>&1
sips -s format jpeg -s formatOptions 90 "$TMP/all-scenes.png" --out "$OUT/all-scenes.jpg" >/dev/null 2>&1

echo "Done! Rendered $(ls "$OUT"/*.jpg | wc -l | tr -d ' ') previews + screenshot.png"
