#!/bin/sh
# Languages for Q2 Pod: the card folder .langs (q2app, the marker q2-langs and lang/*.tsv), zipped as a release
# ships it, dist/langs.zip, to unzip at the card's root or for the App Store to install. The zip is the same bytes
# from build to build. Needs python3.
set -eu
cd "$(dirname "$0")"
rm -rf dist
mkdir -p dist
python3 -I - dist/langs.zip q2app q2-langs lang/*.tsv <<'PY'
import sys, zipfile
with zipfile.ZipFile(sys.argv[1], 'w', zipfile.ZIP_DEFLATED) as z:
    for name in sys.argv[2:]:
        info = zipfile.ZipInfo('.langs/' + name, (2026, 1, 1, 0, 0, 0))
        info.external_attr, info.compress_type = (0o100644 << 16), zipfile.ZIP_DEFLATED
        z.writestr(info, open(name, 'rb').read())
PY
