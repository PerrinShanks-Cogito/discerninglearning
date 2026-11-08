import requests, re, io
import pandas as pd
pd.set_option("display.width",250); pd.set_option("display.max_columns",40); pd.set_option("display.max_colwidth",40)
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
x=pd.ExcelFile(io.BytesIO(s.get("https://assets.publishing.service.gov.uk/media/691b0990d140bbbaa59a28ad/CRA_2025_Chapter_A_tables.xlsx",timeout=120).content))
df=pd.read_excel(x,"A.15",header=None)
hdr=df.iloc[2].tolist(); hcol=[i for i,v in enumerate(hdr) if str(v).strip().startswith("7. Health")][0]; tcol=[i for i,v in enumerate(hdr) if str(v).startswith("Total")][0]
year=None
for i,r in df.iterrows():
    v=str(r[0]).strip()
    if re.match(r"^20\d\d-\d\d",v): year=v
    if v in ("England","Scotland","Wales","Northern Ireland","UK identifiable expenditure"): print("CRA",year,v,"health",r[hcol],"total",r[tcol])
h=pd.ExcelFile(io.BytesIO(s.get("https://www.ons.gov.uk/file?uri=/peoplepopulationandcommunity/healthandsocialcare/healthandlifeexpectancies/datasets/healthstatelifeexpectancyallagesuk/current/healthylifeexpectancyuk.xlsx",timeout=120).content))
for sh in ["Contents","1"]:
    d=pd.read_excel(h,sh,header=None); print("--- SHEET",sh,d.shape); print(d.head(14).to_string())
d=pd.read_excel(h,"1",header=None)
hi=next(i for i in range(15) if d.iloc[i].astype(str).str.contains("Period|Time period|Country|Area name",case=False).any())
d.columns=d.iloc[hi]; d=d.iloc[hi+1:]
print("COLS",list(d.columns))
m=d.astype(str).apply(lambda r: r.str.contains("2022 to 2024").any() and r.str.fullmatch(r"(United Kingdom|England|Wales|Scotland|Northern Ireland)").any(),axis=1)
sub=d[m]
age=[c for c in d.columns if "age" in str(c).lower()]
if age: sub=sub[sub[age[0]].astype(str).str.contains(r"^(<1|0|At birth|Birth|0 to|<1 year)",regex=True)]
print(sub.to_string())
# 1794156266
