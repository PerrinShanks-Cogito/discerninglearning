import requests, io
import pandas as pd
pd.set_option("display.width",400); pd.set_option("display.max_columns",40); pd.set_option("display.max_colwidth",45); pd.set_option("display.max_rows",300)
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
A="https://assets.publishing.service.gov.uk/media/"
files={"5.6":A+"6a6a3616862aaf18d9c629eb/DUKES_5.6.xlsx","5.7":A+"6a6a3622cceb23e8678976bf/DUKES_5.7.xlsx",
"5.13":A+"6a6a3675bf4a7aca8f8976c3/DUKES_5.13.xlsx","5.16":A+"6a6a36a0bf4a7aca8f8976c6/DUKES_5.16.xlsx",
"6.2":A+"6a6a27620c36759b5ccaa1d1/DUKES_6.2.xlsx","REG":A+"6aba6c4afe72ed1e2b02f14b/Regional_Electricity_Generation_and_Supply_Timeseries_2026.xlsx",
"5.11":A+"6a6a365b0ddb7e4831c629f3/DUKES_5.11.xlsx","5.14":A+"6a6a3684bf4a7aca8f8976c4/DUKES_5.14.xlsx"}
for k,u in files.items():
    try:
        x=pd.ExcelFile(io.BytesIO(s.get(u,timeout=180).content))
        print("#####",k,x.sheet_names)
        for sh in x.sheet_names:
            d=pd.read_excel(x,sh,header=None)
            if k=="5.11" and len(d)>200:
                d=d[d.astype(str).apply(lambda r: r.str.contains("Nuclear|Pumped|Technology|Type",case=False).any(),axis=1)]
            d=d.dropna(how="all",axis=1)
            if k in ("5.6","5.7","REG","6.2") and d.shape[1]>12:
                d=pd.concat([d.iloc[:,:2],d.iloc[:,-6:]],axis=1)
            print("=====",k,sh,d.shape); print(d.to_string()[:7000])
    except Exception as e: print("ERR",k,e)
# 1794165397
