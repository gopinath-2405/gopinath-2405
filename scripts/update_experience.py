"""Refresh the experience badges (assets/experience-{dark,light}.svg) and the About me text, counted from Dec 2024."""
import re
from datetime import date
from pathlib import Path

START = date(2024, 12, 2)
ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
BADGES = {
    "dark": (ROOT / "assets" / "experience-dark.svg", "#0f1729", "#94a3b8"),
    "light": (ROOT / "assets" / "experience-light.svg", "#ffffff", "#475569"),
}

MONO = "'SF Mono','JetBrains Mono','Fira Code',ui-monospace,Menlo,Consolas,monospace"
BADGE_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="46" viewBox="0 0 {w} 46" role="img" aria-label="Experience: {long}">
<style>
svg{{--pill:{pill};--muted:{muted}}}
.mono{{font-family:{mono}}}
@keyframes pulse{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
</style>
<defs>
<linearGradient id="b" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#14b8a6"/><stop offset=".5" stop-color="#6366f1"/><stop offset="1" stop-color="#7c3aed"/>
<animateTransform attributeName="gradientTransform" type="rotate" values="0 .5 .5;360 .5 .5" dur="6s" repeatCount="indefinite"/></linearGradient>
<linearGradient id="t" x1="0" x2="1" spreadMethod="reflect"><stop offset="0" stop-color="#14b8a6"/><stop offset=".5" stop-color="#818cf8"/><stop offset="1" stop-color="#14b8a6"/>
<animateTransform attributeName="gradientTransform" type="translate" values="0 0;1 0;0 0" dur="5s" repeatCount="indefinite"/></linearGradient>
<linearGradient id="bg" x1="0" x2="1"><stop offset="0" stop-color="#14b8a6" stop-opacity=".14"/><stop offset="1" stop-color="#6366f1" stop-opacity=".12"/></linearGradient>
</defs>
<rect x="1" y="1" width="{iw}" height="44" rx="22" style="fill:var(--pill)"/>
<rect x="1" y="1" width="{iw}" height="44" rx="22" fill="url(#bg)" stroke="url(#b)" stroke-width="2"/>
<circle cx="24" cy="23" r="5" fill="#14b8a6"/>
<circle cx="24" cy="23" r="9" fill="none" stroke="#14b8a6" stroke-width="1.5"><animate attributeName="r" values="5;12;5" dur="2.4s" repeatCount="indefinite"/><animate attributeName="opacity" values=".9;0;.9" dur="2.4s" repeatCount="indefinite"/></circle>
<text class="mono" x="40" y="23" dominant-baseline="central" font-size="12" font-weight="700" letter-spacing="1.5" style="fill:var(--muted)">EXPERIENCE</text>
<text class="mono" x="{vx}" y="23" dominant-baseline="central" font-size="15" font-weight="800" textLength="{vw}" lengthAdjust="spacingAndGlyphs" fill="url(#t)">{short}</text>
</svg>
"""


def months_since(start: date, today: date) -> int:
    months = (today.year - start.year) * 12 + today.month - start.month
    return months - 1 if today.day < start.day else months


def plural(n: int, word: str) -> str:
    return f"{n} {word}{'' if n == 1 else 's'}"


def duration(months: int, short: bool) -> str:
    years, rest = divmod(months, 12)
    y, m = ("yr", "mo") if short else ("year", "month")
    parts = [plural(years, y)] if years else []
    if rest or not years:
        parts.append(plural(rest, m))
    return " ".join(parts)


def replace(text: str, marker: str, value: str) -> str:
    pattern = re.compile(rf"(<!-- {marker}:START -->).*?(<!-- {marker}:END -->)", re.S)
    if not pattern.search(text):
        raise SystemExit(f"Marker {marker} not found in README.md")
    return pattern.sub(lambda m: m.group(1) + value + m.group(2), text)


def main() -> None:
    months = months_since(START, date.today())
    short, long = duration(months, short=True), duration(months, short=False)

    value_x = 40 + 10 * 12 * 0.6 + 12 * 1.5 + 12
    value_w = len(short) * 15 * 0.6
    width = round(value_x + value_w + 22)
    for path, pill, muted in BADGES.values():
        path.write_text(BADGE_SVG.format(w=width, iw=width - 2, vx=f"{value_x:.1f}", vw=f"{value_w:.1f}",
                                         short=short, long=long, mono=MONO, pill=pill, muted=muted), encoding="utf-8")

    text = README.read_text(encoding="utf-8")
    README.write_text(replace(text, "EXPERIENCE-TEXT", long), encoding="utf-8")
    print(f"Experience: {long}")


if __name__ == "__main__":
    main()
