# Languages

Other languages for [Q2 Pod](https://github.com/DiamondBond/q2-pod), the music player firmware for the Shanling Q2.

Q2 Pod is in English. With this card app installed, System settings shows **Language** again: pick one and the Q2 restarts in it. The language picked is copied to the Q2 itself, so it stays when the card is out or swapped. Removing the app in the App Store sets the Q2 back to English from its next start. A text the language has no line for is shown in English.

Install it from Q2 Pod's App Store (Library → App Store), or unzip `langs.zip` at the card's root (it holds one folder, `.langs`). It has no row of its own: it only adds the Language row.

It also carries an Arabic font, so Arabic, Persian and Urdu titles, artists, albums and lyrics show in any language, English too, right to left with their letters joined. Without it they are blank: no font on the Q2 has those letters.

## Languages

| Language | Table |
| --- | --- |
| Français | `lang/fr.tsv` |
| Deutsch | `lang/de.tsv` |
| Italiano | `lang/it.tsv` |
| 日本語 | `lang/ja.tsv` |
| 한국어 | `lang/ko.tsv` |
| Polski | `lang/pl.tsv` |
| Русский | `lang/ru.tsv` |
| 简体中文 | `lang/zh_CN.tsv` |
| Español | `lang/es.tsv` |
| ภาษาไทย | `lang/th.tsv` |
| 繁體中文 | `lang/zh_HK.tsv` |
| Українська | `lang/uk.tsv` |

## A table

`lang/<code>.tsv` is UTF-8. Its first line is `# ` and the language's own name, which the Language page lists. Each other line is one text, three fields between tabs:

```
key	English	translation
```

The key and the English are what Q2 Pod asks for, copied from `en.tsv`; the translation is yours. Write a line break as `\n`, a tab as `\t` and a backslash as `\\`. A `%d`, `%s` or other conversion in the English stays in the translation, in the same order. A line whose English Q2 Pod no longer uses, or whose conversions differ from its English's, is skipped and that text shows in English, so an old table never breaks a newer Q2 Pod.

Two things the Q2 does with your text: a settings row whose English is `Title: value` (`Shortcut: %s`) is split at its `": "` into a label and a value, so keep that ASCII `": "` in those rows; and of a count's two lines (`%u song`, `%u songs`), the first shows for exactly 1 and the second for every other number, so in a language with more plural forms word the second to fit any of them (`Songs: %u`). One English text of Q2 Pod's own has one translation everywhere it shows.

`en.tsv` lists every text Q2 Pod shows, made from a build with Q2 Pod's `tools/langpack.py template BUILD`. Check a table against it, and against the Q2's font, before sending it:

```
python3 tools/langpack.py check en.tsv lang/de.tsv default.ttf
```

It names each line the Q2 would skip and each character the font lacks, then how many texts the table leaves in English.

## Building

`./build.sh` makes `dist/langs.zip`, the same bytes from build to build. It needs Python 3 with fontTools (`PYTHON=` names another Python), which `tools/font.py` uses to make `lang/font.ttf` from Noto Sans Arabic UI: cut to the characters Q2 Pod asks a pack's font for, and sized to the Q2's own face.

## Credits

The Simplified Chinese table started from gukey's, in Q2 Pod's pull request #452.

## License

GPL-3.0, as Q2 Pod. The font is Noto Sans Arabic UI (`fonts/`), under the SIL Open Font License 1.1, whose text the zip carries beside it.
