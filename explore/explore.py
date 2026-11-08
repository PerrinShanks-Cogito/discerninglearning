import requests, io
import pandas as pd
pd.set_option("display.width",400); pd.set_option("display.max_columns",40); pd.set_option("display.max_colwidth",60); pd.set_option("display.max_rows",300)
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
A="https://assets.publishing.service.gov.uk/media/"
def X(u): return pd.ExcelFile(io.BytesIO(s.get(u,timeout=180).content))
x=X(A+"6aba6c4afe72ed1e2b02f14b/Regional_Electricity_Generation_and_Supply_Timeseries_2026.xlsx")
for sh in ["Generation and supply","Electricity generation by fuel"]:
    d=pd.read_excel(x,sh,header=None)
    hdr=None
    for i,r in d.iterrows():
        if any("2025" in str(v) for v in r.tolist()): hdr=i; break
    cols=[c for c in d.columns if "2025" in str(d.iat[hdr,c])]
    lab=[c for c in d.columns[:2]]
    print("=====",sh); print(d.iloc[:,lab+cols].to_string())
x=X(A+"6a6a3675bf4a7aca8f8976c3/DUKES_5.13.xlsx"); d=pd.read_excel(x,"5.13",header=None)
for i in range(len(d)):
    if str(d.iat[i,0]).strip()=="Year": print("HDR", list(enumerate(d.iloc[i].tolist())))
    if str(d.iat[i,0]).startswith("2025"): print("2025", list(enumerate(d.iloc[i].tolist())))
x=X(A+"6a6a365b0ddb7e4831c629f3/DUKES_5.11.xlsx"); d=pd.read_excel(x,"5.11 Full list",header=None)
print(d.head(8).to_string()[:3000])
m=d[d.astype(str).apply(lambda r: r.str.contains("Nuclear|Pumped",case=False).any(),axis=1)]
print(m.to_string()[:6000])
for p in ["/government/statistics/natural-gas-chapter-4-digest-of-united-kingdom-energy-statistics-dukes","/government/statistics/regional-renewable-statistics","/government/statistics/energy-trends-section-4-gas"]:
    try:
        j=s.get("https://www.gov.uk/api/content"+p,timeout=60).json(); print("#####",p,j.get("public_updated_at"))
        for a in j.get("details",{}).get("attachments",[]): print("  ",a.get("title"),"|",a.get("url"))
    except Exception as e: print("ERR",p,e)
# 1794165516
