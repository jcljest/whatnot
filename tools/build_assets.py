"""Regenerate the color-break SVGs from one template.

Edit COLORS or the templates below, then run:  python tools/build_assets.py
Each tile is a standalone 118x176 SVG, so OBS can hide/move every color on its own.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / 'assets'
FONT = "'SF Pro Display','Segoe UI',Arial,sans-serif"
YELLOW, INK, PANEL, SLOT = '#FFE000', '#0F0F0F', '#161616', '#3A3A3A'  # Whatnot yellow is approximate

# key, label, letter, dot fill, letter fill, optional dot ring, label size
COLORS = [
    ('white',     'WHITE',     'W', '#F4EFD9', INK,       None,      20),
    ('blue',      'BLUE',      'U', '#1E73BE', '#FFFFFF', None,      20),
    ('black',     'BLACK',     'B', '#1C1A1A', '#E8E2D6', '#E8E2D6', 20),
    ('red',       'RED',       'R', '#D7262E', '#FFFFFF', None,      20),
    ('green',     'GREEN',     'G', '#1B8A4B', '#FFFFFF', None,      20),
    ('multi',     'MULTI',     'M', '#C9A23F', INK,       None,      20),
    ('colorless', 'COLORLESS', 'C', '#C8C3BC', INK,       None,      17),
    ('lands',     'LANDS',     'L', '#8B6B4A', '#FFFFFF', None,      20),
]

TILE = '''<?xml version="1.0" encoding="UTF-8"?>
<!-- Color break tile: {label}. 118x176. Buyer name is an OBS text source in the empty slot (y 128-162). -->
<svg xmlns="http://www.w3.org/2000/svg" width="118" height="176" viewBox="0 0 118 176" font-family="{font}">
  <defs><clipPath id="shape"><rect width="118" height="176" rx="14"/></clipPath></defs>
  <rect width="118" height="176" rx="14" fill="{panel}" fill-opacity="0.94"/>
  <rect width="118" height="6" fill="{strip}" clip-path="url(#shape)"/>
  <circle cx="59" cy="50" r="34" fill="{dot}"{ring}/>
  <text x="59" y="63" font-size="36" font-weight="800" fill="{letter_fill}" text-anchor="middle">{letter}</text>
  <text x="59" y="116" font-size="{size}" font-weight="800" fill="#FFFFFF" text-anchor="middle">{label}</text>
  <rect x="19" y="164" width="80" height="2" rx="1" fill="{slot}"/>
</svg>
'''

HEADER = '''<?xml version="1.0" encoding="UTF-8"?>
<!-- Color break header. 300x64. -->
<svg xmlns="http://www.w3.org/2000/svg" width="300" height="64" viewBox="0 0 300 64" font-family="{font}">
  <defs><clipPath id="shape"><rect width="300" height="64" rx="16"/></clipPath></defs>
  <rect width="300" height="64" rx="16" fill="{panel}" fill-opacity="0.94"/>
  <rect width="300" height="6" fill="{yellow}" clip-path="url(#shape)"/>
  <text x="150" y="47" font-size="34" font-weight="800" fill="{yellow}" text-anchor="middle" letter-spacing="2">COLOR BREAK</text>
</svg>
'''

OUT.mkdir(exist_ok=True)
(OUT / 'cb-header.svg').write_text(HEADER.format(font=FONT, panel=PANEL, yellow=YELLOW), encoding='utf-8')
for key, label, letter, dot, letter_fill, ring, size in COLORS:
    ring_attr = f' stroke="{ring}" stroke-width="3"' if ring else ''
    svg = TILE.format(font=FONT, panel=PANEL, slot=SLOT, label=label, letter=letter, dot=dot,
                      letter_fill=letter_fill, ring=ring_attr, size=size, strip=ring or dot)
    (OUT / f'cb-tile-{key}.svg').write_text(svg, encoding='utf-8')
print(f'Wrote header + {len(COLORS)} tiles to {OUT}')
