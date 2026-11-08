import requests, io
import pandas as pd
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
A="https://assets.publishing.service.gov.uk/media/"
files={"5.6":(A+"6a6a3616862aaf18d9c629eb/DUKES_5.6.xlsx",["5.6"]),"5.7":(A+"6a6a3622cceb23e8678976bf/DUKES_5.7.xlsx",["5.7"]),
"5.13":(A+"6a6a3675bf4a7aca8f8976c3/DUKES_5.13.xlsx",["5.13","5.13A"]),"5.16":(A+"6a6a36a0bf4a7aca8f8976c6/DUKES_5.16.xlsx",["5.16"]),
"6.2":(A+"6a6a27620c36759b5ccaa1d1/DUKES_6.2.xlsx",["6.2"]),"REG":(A+"6aba6c4afe72ed1e2b02f14b/Regional_Electricity_Generation_and_Supply_Timeseries_2026.xlsx",["Generation and supply","Electricity generation by fuel"]),
"5.11":(A+"6a6a365b0ddb7e4831c629f3/DUKES_5.11.xlsx",["5.11 Summary"]),"5.14":(A+"6a6a3684bf4a7aca8f8976c4/DUKES_5.14.xlsx",["5.14"])}
def f(v):
    if isinstance(v,float): return f"{v:.1f}"
    return str(v)[:60]
for k,(u,sheets) in files.items():
    x=pd.ExcelFile(io.BytesIO(s.get(u,timeout=180).content))
    for sh in sheets:
        d=pd.read_excel(x,sh,header=None).dropna(how="all",axis=1)
        print("=====",k,sh,d.shape)
        wide=d.shape[1]>12
        for _,r in d.iterrows():
            vals=[v for v in r.tolist() if not (isinstance(v,float) and pd.isna(v))]
            if not vals: continue
            txt=[v for v in vals if isinstance(v,str)]; num=[v for v in vals if not isinstance(v,str)]
            if k in ("5.13","5.16","5.14") and wide:
                print(" | ".join(f(v) for v in vals)[:900])
            else:
                print(" | ".join(t[:55] for t in txt[:3]),"::"," ".join(f(v) for v in num[-3:]))
# 1794165446
