import requests, io, re, time
import pandas as pd
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
def get(u):
    for k in range(6):
        r=s.get(u,timeout=180); print("GET",u[:120],r.status_code,len(r.content))
        if r.status_code!=429: return r
        time.sleep(40)
    return r
import pdfplumber
r=get("https://research.ftserussell.com/analytics/factsheets/Home/DownloadConstituentsWeights/?indexdetails=UKX")
with pdfplumber.open(io.BytesIO(r.content)) as pdf:
    txt="\n".join((p.extract_text() or "") for p in pdf.pages)
rows=re.findall(r"([A-Z0-9][A-Za-z0-9&'().,\- ]+?) (\d+\.\d+) UNITED KINGDOM",txt)
w=sorted(((float(b),a.strip()) for a,b in rows),reverse=True)
print("constituents parsed",len(w)); print("TOP12",w[:12]); print("sum",round(sum(x for x,_ in w),2))
time.sleep(3)
u="https://www.ons.gov.uk/file?uri=/economy/grossvalueaddedgva/datasets/nominalandrealregionalgrossvalueaddedbalancedbyindustry/current/regionalgrossvalueaddedbalancedbyindustryandallinternationalterritoriallevelsitlregions.xlsx"
x=pd.ExcelFile(io.BytesIO(get(u).content))
names={"United Kingdom","England","Scotland","Wales","Northern Ireland"}
def tbl(sh):
    d=pd.read_excel(x,sh,header=1)
    d.columns=[str(c).replace(".0","") for c in d.columns]
    return d[d["Region name"].isin(names)]
cp=tbl("Table 1c"); ix=tbl("Table 1a")
sec=cp[cp["SIC07 code"].astype(str).str.match(r"^([A-T]( \(.*\))?|Total)$")]
print("== current prices 2024, £m, sections")
print(sec.pivot_table(index=["SIC07 code","SIC07 description"],columns="Region name",values="2024",aggfunc="first").to_string())
isec=ix[(ix["Region name"]=="United Kingdom")&(ix["SIC07 code"].astype(str).str.match(r"^([A-T]( \(.*\))?|Total)$"))]
print("== UK CVM index 2014, 2019, 2024")
print(isec[["SIC07 code","SIC07 description","2014","2019","2024"]].to_string())
# finer industries with biggest real growth 2019-2024 (UK, 2-digit or groups) with 2024 size
fine=ix[(ix["Region name"]=="United Kingdom")][["SIC07 code","SIC07 description","2019","2024"]].copy()
fine["g"]=(fine["2024"]/fine["2019"]-1)*100
cpu=cp[cp["Region name"]=="United Kingdom"][["SIC07 code","2024"]].rename(columns={"2024":"cp2024"})
fine=fine.merge(cpu,on="SIC07 code")
print("== fastest real growth 2019-24 (industries with >= £10bn GVA in 2024)")
print(fine[fine.cp2024>=10000].sort_values("g",ascending=False).head(15).to_string())
time.sleep(3)
u2="https://www.ons.gov.uk/file?uri=/economy/grossdomesticproductgdp/datasets/regionalgrossdomesticproductallnutslevelregions/1998to2024/regionalgrossdomesticproductgdpbyallinternationalterritoriallevelitlregions.xlsx"
x2=pd.ExcelFile(io.BytesIO(get(u2).content))
c=pd.read_excel(x2,"Contents",header=None); print(c.iloc[:16].to_string()[:2000])
for sh in ["Table 5","Table 6","Table 7"]:
    d=pd.read_excel(x2,sh,header=1); d.columns=[str(cc).replace(".0","") for cc in d.columns]
    nm=[cc for cc in d.columns if "name" in cc.lower()][0]
    print("==",sh); print(d[d[nm].isin(names)].iloc[:, :3].join(d[d[nm].isin(names)][["2023","2024"]]).to_string())
# 1794174893
