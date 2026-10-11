"""Tidy Pandoc's Markdown for a Word document before it goes on the site.

Usage: python3 tidy-markdown.py document.docx < pandoc.md > tidy.md

- A short bold ALL-CAPS line at the very top (e.g. "DATA WORK · CASE STUDY")
  becomes a small label above the content.
- Paragraphs in Word's Title or Subtitle style become a subtitle. (Pandoc only
  treats Title as the page title when it is the first thing in the document;
  anywhere else it would come out as plain text.)
- Tables with an empty first row, which Pandoc writes for Word tables that
  have no header row, lose that row.
- Table cells that start with a short bold figure such as "+17%" become
  "headline figure" tiles.
"""
import html
import re
import sys
import zipfile

docx = sys.argv[1]
md = sys.stdin.read()


def plain(text):
    """Text as a reader sees it: no Markdown escapes, entities or spacing."""
    text = re.sub(r"\\(.)", r"\1", text)
    return " ".join(html.unescape(text).split())


# Text of Title/Subtitle-styled paragraphs in the Word document.
with zipfile.ZipFile(docx) as z:
    doc = z.read("word/document.xml").decode("utf-8")
subtitles = set()
for para in re.findall(r"<w:p[ >].*?</w:p>", doc, re.S):
    if re.search(r'<w:pStyle w:val="(Title|Subtitle)"', para):
        text = plain("".join(re.findall(r"<w:t(?: [^>]*)?>([^<]*)</w:t>", para)))
        if text:
            subtitles.add(text)

blocks = md.split("\n\n")
out = []
for i, block in enumerate(blocks):
    stripped = block.strip()
    kicker = re.fullmatch(r"\*\*([^*\n]{1,60})\*\*", stripped)
    if not out and kicker and kicker.group(1) == kicker.group(1).upper() and re.search(r"[A-Z]", kicker.group(1)):
        block = '<p class="doc-kicker">%s</p>' % html.escape(plain(kicker.group(1)))
    elif "\n" not in stripped and plain(stripped) in subtitles:
        block = '<p class="doc-subtitle">%s</p>' % html.escape(plain(stripped))
    out.append(block)
md = "\n\n".join(out)

# Drop an empty header row (and its separator) from Markdown tables.
md = re.sub(r"^\|(?:[ \t]*\|)+[ \t]*\n\|[-:| \t]+\|[ \t]*\n", "", md, flags=re.M)

# Headline figures: <td><p><strong>+17%</strong></p> ... in an HTML table.
FIGURE = r"<td><p><strong>([^<]{1,10}\d[^<]{0,10})</strong></p>"


def figures(match):
    table = match.group(0)
    if not re.search(FIGURE, table):
        return table
    table = re.sub(r"<colgroup>.*?</colgroup>\n?", "", table, flags=re.S)
    table = table.replace("<table>", '<table class="stat-table">', 1)
    return re.sub(FIGURE, r'<td><p class="stat-figure">\1</p>', table)


md = re.sub(r"<table>.*?</table>", figures, md, flags=re.S)
sys.stdout.write(md)
