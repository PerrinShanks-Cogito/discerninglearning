import requests, io
import pandas as pd
pd.set_option("display.width",400); pd.set_option("display.max_columns",40); pd.set_option("display.max_colwidth",70); pd.set_option("display.max_rows",300)
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
A="https://assets.publishing.service.gov.uk/media/"
def X(u): return pd.ExcelFile(io.BytesIO(s.get(u,timeout=180).content))
def show(u, sheets=None, key="2025", find="UK Total|England|Scotland"):
    x=X(u); print("#####",u.split("/")[-1],x.sheet_names)
    for sh in (sheets or x.sheet_names):
        if sh in ("Cover Sheet","Contents","Notes","Cover sheet"): continue
        d=pd.read_excel(x,sh,header=None)
        hdr=next((i for i,r in d.iterrows() if sum(key in str(v) for v in r.tolist())>=2), None)
        if hdr is None: print("== no hdr",sh, d.shape); print(d.head(12).to_string()[:2500]); continue
        cols=[c for c in d.columns if key in str(d.iat[hdr,c])]
        lab=[c for c in d.columns[:3] if c not in cols]
        print("=====",sh,"hdr row",hdr); print(d.iloc[hdr:, lab+cols].dropna(how="all").to_string(max_colwidth=60)[:9000])
show(A+"6aba6c4afe72ed1e2b02f14b/Regional_Electricity_Generation_and_Supply_Timeseries_2026.xlsx",["Generation and supply","Electricity generation by fuel"])
show(A+"6aba6ee6997a4b2950ccefec/Regional_installed_capacity_MW_2003-2025.xlsx")
show(A+"6aba6ef6fe72ed1e2b02f152/Regional_generation_GWh_2003-2025.xlsx")
x=X(A+"6a69f47e701b2d693e5b9420/DUKES_4.1.1.xlsx"); print("##### 4.1.1",x.sheet_names)
for sh in x.sheet_names[3:]:
    d=pd.read_excel(x,sh,header=None); print("==",sh); print(d.iloc[:12].to_string()[:2500]); print(d.tail(4).to_string()[:2500])
x=X(A+"6aba96a9734e2435f202f1d6/DUKES_4.5.xlsx"); print("##### 4.5",x.sheet_names)
for sh in x.sheet_names[3:]:
    d=pd.read_excel(x,sh,header=None).dropna(how="all",axis=1); print("==",sh,d.shape)
    print(pd.concat([d.iloc[:,:2],d.iloc[:,-2:]],axis=1).to_string()[:5000])
# 1794165564
