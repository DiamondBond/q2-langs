"""lang/font.ttf, made by build.sh: Noto Sans Arabic UI Regular (fonts/, OFL, no Reserved Font Name) cut to the
characters Q2 Pod asks a language pack's font for (its tools/build.py GLYPH_FALLBACK: right-to-left scripts,
their presentation forms and the zero-width controls), each control an empty glyph with no advance (a lam-alef's
U+FEFF filler among them), and its line set to the stock face's, ascent 230 and descent -69 of 256:
stb scales a face to a pixel height by them, so these letters come out as big as stock's.

    python3 tools/font.py fonts/NotoSansArabicUI-Regular.ttf out.ttf"""
import sys

from fontTools import subset
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont

RANGES = ((0x0590, 0x08ff), (0x200b, 0x200f), (0x2066, 0x2069), (0xfb1d, 0xfdff), (0xfe70, 0xfeff))
ZERO_WIDTH = (0x061c, *range(0x200b, 0x2010), *range(0x2066, 0x206a), 0xfeff)
STOCK_EM, STOCK_ASCENT, STOCK_DESCENT = 256, 230, -69


def cut(src):
    font = TTFont(src, recalcTimestamp=False)
    options = subset.Options()
    options.layout_features, options.name_IDs, options.notdef_outline = [], ['*'], True
    options.drop_tables += ['GSUB', 'GPOS', 'GDEF']  # stb draws a glyph a character: FriBidi shapes before
    sub = subset.Subsetter(options)
    sub.populate(unicodes=[u for u in font.getBestCmap() if any(a <= u <= b for a, b in RANGES)])
    sub.subset(font)
    font['glyf']['zero'], font['hmtx']['zero'] = TTGlyphPen(None).glyph(), (0, 0)
    for table in font['cmap'].tables:  # Noto's own U+061C has an advance
        if table.isUnicode():
            table.cmap.update({u: 'zero' for u in ZERO_WIDTH})
    em = font['head'].unitsPerEm
    ascent, descent = round(STOCK_ASCENT * em / STOCK_EM), round(STOCK_DESCENT * em / STOCK_EM)
    font['hhea'].ascent, font['hhea'].descent, font['hhea'].lineGap = ascent, descent, 0
    os2 = font['OS/2']
    os2.sTypoAscender, os2.sTypoDescender, os2.sTypoLineGap = ascent, descent, 0
    os2.usWinAscent, os2.usWinDescent = ascent, -descent
    return font


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    font = cut(sys.argv[1])
    cmap = font.getBestCmap()
    assert all(u in cmap for u in range(0xfe80, 0xfefd)) and all(font['hmtx'][cmap[u]][0] == 0 for u in ZERO_WIDTH)
    font.save(sys.argv[2], reorderTables=False)
