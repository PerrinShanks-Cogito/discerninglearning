import requests, re, io, html
import pandas as pd
pd.set_option("display.width",250); pd.set_option("display.max_columns",30); pd.set_option("display.max_colwidth",45)
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
def page(u):
    r=s.get(u,timeout=90); return r.status_code, html.unescape(re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",re.sub(r"(?s)<(script|style).*?</\1>","",r.text)))), r.text
N="https://www.nomisweb.co.uk/api/v01/dataset/"
for ds in ["NM_30_1","NM_99_1"]:
    r=s.get(f"{N}{ds}.data.csv?geography=TYPE499&date=2026&sex=8&item=2&pay=1&measures=20100&select=date_name,geography_name,obs_value,obs_status_name",timeout=90)
    print("ASHE2026",ds,r.status_code,r.text[:700])
c,t,_=page("https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/bulletins/regionallabourmarket/october2026")
i=t.find("Table 1: Summary of latest headline estimates"); print("LMTABLE",t[i:i+2600])
j=t.find("Release date"); print("LMDATE",t[j:j+80])
# HLE dataset
c,t,raw=page("https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthandlifeexpectancies/datasets/healthstatelifeexpectancyallagesuk")
links=[l for l in re.findall(r'href="([^"]+\.xlsx)"',raw)]; print("HLELINKS",links[:5])
if links:
    u=links[0] if links[0].startswith("http") else "https://www.ons.gov.uk"+links[0]
    x=pd.ExcelFile(io.BytesIO(s.get(u,timeout=120).content)); print("SHEETS",x.sheet_names)
    for sh in x.sheet_names:
        df=pd.read_excel(x,sh,header=None)
        if df.shape[0]<20: continue
        print("--- SHEET",sh,df.shape); print(df.head(8).to_string())
        mask=df.astype(str).apply(lambda r: r.str.contains("2022 to 2024|2022-2024|2022-24").any() and r.str.contains(r"^(United Kingdom|England|Wales|Scotland|Northern Ireland)$").any(),axis=1)
        print(df[mask].head(40).to_string())
        break
# CRA chapter A tables
x=pd.ExcelFile(io.BytesIO(s.get("https://assets.publishing.service.gov.uk/media/691b0990d140bbbaa59a28ad/CRA_2025_Chapter_A_tables.xlsx",timeout=120).content))
print("CRASHEETS",x.sheet_names)
for sh in x.sheet_names:
    df=pd.read_excel(x,sh,header=None)
    title=" ".join(str(v) for v in df.iloc[:4,0].tolist())
    if re.search(r"per head",title,re.I) and re.search(r"function",title,re.I):
        print("=== ",sh,title[:200])
        hm=df.astype(str).apply(lambda r: r.str.contains(r"^\s*(Health|Total|Country|of which|England|Scotland|Wales|Northern Ireland|UK identifiable)",regex=True).any(),axis=1)
        print(df.head(10).to_string()); print(df[hm].head(30).to_string())
# 1794156217
