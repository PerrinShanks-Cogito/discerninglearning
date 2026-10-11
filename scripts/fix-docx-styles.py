"""Make a .docx readable by Pandoc's heading detection.

Some tools that generate Word files base their Heading and Title styles on a
"Normal" style that the file never defines. Word copes, but Pandoc then
ignores every heading style. If Normal is missing, write a copy of the
document with it added.

Usage: python3 fix-docx-styles.py in.docx out.docx
Prints "fixed" if a change was made, otherwise copies the file unchanged.
"""
import re
import shutil
import sys
import zipfile

NORMAL = ('<w:style w:type="paragraph" w:default="1" w:styleId="Normal">'
          '<w:name w:val="Normal"/><w:qFormat/></w:style>')

src, dst = sys.argv[1], sys.argv[2]
with zipfile.ZipFile(src) as z:
    styles = z.read("word/styles.xml").decode("utf-8") if "word/styles.xml" in z.namelist() else None

if styles is None or re.search(r'w:styleId="Normal"', styles):
    shutil.copyfile(src, dst)
    sys.exit(0)

# Insert the style after <w:docDefaults>, or else straight after <w:styles ...>.
if "</w:docDefaults>" in styles:
    styles = styles.replace("</w:docDefaults>", "</w:docDefaults>" + NORMAL, 1)
else:
    styles = re.sub(r"(<w:styles\b[^>]*>)", r"\1" + NORMAL, styles, count=1)

with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = styles.encode("utf-8") if item.filename == "word/styles.xml" else zin.read(item.filename)
        zout.writestr(item, data)
print("fixed")
