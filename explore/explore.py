import requests, io, re, time
import pandas as pd
pd.set_option("display.width",320); pd.set_option("display.max_columns",40); pd.set_option("display.max_colwidth",50); pd.set_option("display.max_rows",200)
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
def get(u):
    for k in range(5):
        r=s.get(u,timeout=180); print("GET",u[:150],r.status_code,len(r.content))
        if r.status_code!=429: return r
        time.sleep(30)
    return r
# FTSE 100 constituents and weights
import pdfplumber
r=get("https://research.ftserussell.com/analytics/factsheets/Home/DownloadConstituentsWeights/?indexdetails=UKX")
if r.content[:4]==b"%PDF":
    with pdfplumber.open(io.BytesIO(r.content)) as pdf:
        txt="\n".join((p.extract_text() or "") for p in pdf.pages[:4])
    print(txt[:3500])
else: print(r.text[:500])
time.sleep(5)
# Regional GVA by industry: nominal and real
u="https://www.ons.gov.uk/file?uri=/economy/grossvalueaddedgva/datasets/nominalandrealregionalgrossvalueaddedbalancedbyindustry/current/regionalgrossvalueaddedbalancedbyindustryandallinternationalterritoriallevelsitlregions.xlsx"
x=pd.ExcelFile(io.BytesIO(get(u).content)); print("sheets",x.sheet_names)
c=pd.read_excel(x,"Contents",header=None); print(c.to_string()[:2500])
want={"UK","United Kingdom","England","Scotland","Wales","Northern Ireland"}
for sh in x.sheet_names:
    if not sh.startswith("Table"): continue
    d=pd.read_excel(x,sh,header=None)
    hdr=next(i for i in range(10) if d.iloc[i].astype(str).str.contains("SIC07").any())
    cols=d.iloc[hdr].tolist()
    body=d.iloc[hdr+1:]
    namecol=[i for i,cn in enumerate(cols) if str(cn).lower().startswith("region name") or str(cn).lower()=="itl region name"]
    nc=namecol[0] if namecol else 2
    sub=body[body.iloc[:,nc].astype(str).isin(want)]
    print("=====",sh,d.iat[0,0][:150]); print("cols",cols[:6],cols[-4:])
    yrs=[i for i,cn in enumerate(cols) if str(cn).startswith(("2019","2023","2024"))]
    keep=[i for i in range(len(cols)) if i<=5]+yrs
    sub2=sub[sub.iloc[:,nc].astype(str).isin({"United Kingdom","UK"})] if sh in ("Table 1","Table 2") else sub[sub.iloc[:,[i for i,cn in enumerate(cols) if 'SIC07 code' in str(cn) or str(cn)=='SIC07 code'][:1] or [3]].astype(str).iloc[:,0].isin(["Total"])]
    print(sub.iloc[:,keep].head(3).to_string()[:800])
    print("-- UK rows")
    print(body[body.iloc[:,nc].astype(str).isin({"United Kingdom","UK"})].iloc[:,keep].to_string()[:5000])
    if sh=="Table 2": break
# 1794174814
