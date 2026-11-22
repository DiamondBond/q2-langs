#!/bin/sh
# Languages for Q2 Pod: the card folder .langs (q2app, the marker q2-langs, lang/*.tsv and the Arabic font
# tools/font.py makes, with its licence), zipped as a release ships it, dist/langs.zip, to unzip at the card's
# root or for the App Store to install. The zip is the same bytes from build to build. Needs python3 with
# fontTools (PYTHON names another).
set -eu
cd "$(dirname "$0")"
PYTHON=${PYTHON:-python3}
R=dist/.langs
rm -rf dist
mkdir -p "$R/lang"
cp q2app q2-langs "$R/"
cp lang/*.tsv "$R/lang/"
"$PYTHON" tools/font.py fonts/NotoSansArabicUI-Regular.ttf "$R/lang/font.ttf"
cp fonts/NotoSansArabic-OFL.txt "$R/lang/font-OFL.txt"
cd dist
"$PYTHON" -I - langs.zip <<'PY'
import pathlib, sys, zipfile
with zipfile.ZipFile(sys.argv[1], 'w', zipfile.ZIP_DEFLATED) as z:
    for path in sorted(p for p in pathlib.Path('.langs').rglob('*') if p.is_file()):
        info = zipfile.ZipInfo(path.as_posix(), (2026, 1, 1, 0, 0, 0))
        info.external_attr, info.compress_type = 0o100644 << 16, zipfile.ZIP_DEFLATED
        z.writestr(info, path.read_bytes())
PY
