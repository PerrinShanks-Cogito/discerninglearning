import requests, io
import pandas as pd
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
A="https://assets.publishing.service.gov.uk/media/"
x=pd.ExcelFile(io.BytesIO(s.get(A+"69ccdb9ab50f8f8dfb8559b3/2025-provisional-greenhouse-gas-emissions-statistics-data-tables.xlsx",timeout=180).content))
d=pd.read_excel(x,"5",header=None).dropna(how="all",axis=1).dropna(how="all")
for _,r in d.iterrows():
    v=[str(a)[:70] for a in r.tolist() if str(a)!="nan"]; print(" | ".join(v[:2]+v[-4:]))
x=pd.ExcelFile(io.BytesIO(s.get(A+"6a3bacc7eaee00074150f326/2005-24-uk-local-authority-ghg-emissions.xlsx",timeout=300).content))
c=pd.read_excel(x,"Contents",header=None)
for _,r in c.iterrows(): print("C:", " | ".join(str(a)[:150] for a in r.tolist() if str(a)!="nan"))
for sh in ["1_1","1_2","2_1","3_1","3_2","4_1","4_2"]:
    d=pd.read_excel(x,sh,header=None)
    hdr=next(i for i in range(min(15,len(d))) if d.iloc[i].astype(str).str.contains("Year|year|Region|Country").any())
    cols=[str(a) for a in d.iloc[hdr].tolist()]
    print("=====",sh,"hdr",hdr); print(cols)
    body=d.iloc[hdr+1:]
    mask=body.astype(str).apply(lambda r: r.str.fullmatch(r"(England|Scotland|Wales|Northern Ireland|Unallocated.*|UK|United Kingdom|National Total|Total.*)").any(),axis=1)
    yr=body.astype(str).apply(lambda r: r.str.fullmatch(r"2024(\.0)?").any(),axis=1)
    sel=body[mask & yr] if (mask & yr).any() else body[mask]
    for _,r in sel.head(12).iterrows():
        print(" ;; ".join(f"{cols[i]}={v}" for i,v in enumerate(r.tolist()) if str(v)!="nan")[:3000])
    if sh in ("3_1","3_2","4_1","4_2"): print(d.to_string()[:4000])
# 1794166489
