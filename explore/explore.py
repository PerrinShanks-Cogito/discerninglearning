import requests, io, re, html, traceback
import pandas as pd
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
try:
    x=pd.ExcelFile(io.BytesIO(s.get("https://www.communities-ni.gov.uk/system/files/2026-08/dfc-ni-uc-stats-supp-tables-may-2026.ods",timeout=120).content),engine="odf")
    d=pd.read_excel(x,"01",header=None); print(d.iloc[55:66,:3].to_string())
except Exception: traceback.print_exc()
# MoD spending in Spending Review 2025 table
try:
    r=s.get("https://www.gov.uk/government/publications/spending-review-2025-document/spending-review-2025-html",timeout=90)
    t=html.unescape(re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",r.text)))
    for m in re.finditer(r"Table [0-9.]+: Ministry of Defence[^.]{0,900}",t): print("SR",m.group(0)[:900])
    for m in re.finditer(r"Defence (Resource DEL|budget|spending)[^.]{0,400}",t): print("SRD",m.group(0)[:400])
except Exception: traceback.print_exc()
# 1794158967
