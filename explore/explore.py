import requests, re, io, traceback
import pandas as pd
pd.set_option("display.width",300); pd.set_option("display.max_columns",60); pd.set_option("display.max_colwidth",70)
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
r=s.get("https://obr.uk/download/public-finances-databank-october-2026-efo/",timeout=180)
x=pd.ExcelFile(io.BytesIO(r.content))
d=pd.read_excel(x,"Aggregates (£bn)",header=None)
hdr=3
for i in range(d.shape[0]):
    if d.iloc[i].astype(str).str.contains(r"^202[4-7]-2[5-8]$").any():
        print("ROW",i,[ (str(d.iloc[hdr,c])[:40], d.iloc[i,c]) for c in range(d.shape[1]) if pd.notna(d.iloc[i,c])][:16])
# notes about outturn/forecast
for sh in ["Aggregates (£bn)","Receipts (£bn)"]:
    d=pd.read_excel(x,sh,header=None)
    for i in range(d.shape[0]):
        for v in d.iloc[i].tolist():
            if isinstance(v,str) and re.search(r"outturn|forecast|Source|EFO",v,re.I): print(sh,"NOTE",i,v[:300])
d=pd.read_excel(x,"Public finances since 1900",header=None); print(d.iloc[0:4].to_string()[:800])
# 1794160021
