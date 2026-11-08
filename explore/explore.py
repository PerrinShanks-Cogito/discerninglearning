import requests, re, io, traceback
import pandas as pd
pd.set_option("display.width",300); pd.set_option("display.max_columns",60); pd.set_option("display.max_colwidth",55)
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
try:
    r=s.get("https://obr.uk/download/public-finances-databank-october-2026-efo/",timeout=180,allow_redirects=True)
    print(r.status_code, r.headers.get("content-type"), len(r.content), r.url)
    x=pd.ExcelFile(io.BytesIO(r.content)); print(x.sheet_names)
    for sh in x.sheet_names:
        d=pd.read_excel(x,sh,header=None)
        print("--",sh,d.shape); print(d.iloc[:6,:8].to_string()[:1200])
    for sh in x.sheet_names:
        if re.search(r"receipt",sh,re.I):
            d=pd.read_excel(x,sh,header=None)
            row=None
            for i in range(d.shape[0]):
                if d.iloc[i].astype(str).str.contains(r"^2025-26$").any(): row=i
            hdr=next((i for i in range(15) if d.iloc[i].astype(str).str.contains("Income tax|income tax",regex=True).any()),None)
            print("== RECEIPTS",sh,"hdr",hdr,"row",row)
            if hdr is not None and row is not None:
                for c in range(d.shape[1]):
                    print("   ",repr(d.iloc[hdr,c]),"|",d.iloc[row,c])
except Exception: traceback.print_exc()
# 1794159967
