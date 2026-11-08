import requests, re, io, html
import pandas as pd
pd.set_option("display.width",250); pd.set_option("display.max_columns",30); pd.set_option("display.max_colwidth",40)
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
N="https://www.nomisweb.co.uk/api/v01/dataset/"
# Working-age population from mid-year estimates (NM_2002_1)
r=s.get(f"{N}NM_2002_1/c_age.def.sdmx.json",timeout=90)
ages=re.findall(r'"description" :\{"value" :"([^"]+)","lang" :"en"\},"value" :(\d+)',r.text)
print("AGES", [a for a in ages if re.search(r"16|64|65|working|All",a[0])][:30])
for q in ["date=latest","date=2025"]:
    r=s.get(f"{N}NM_2002_1.data.csv?geography=TYPE499&{q}&gender=0&c_age=200,203,209&measures=20100&select=date_name,geography_name,c_age_name,obs_value",timeout=90)
    print("MYE",q,r.status_code); print(r.text[:1500])
# Households dataset (LFS)
c=s.get("https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/families/datasets/householdsbyhouseholdsizeregionsofenglandandgbconstituentcountries",timeout=90)
links=re.findall(r'href="([^"]+\.xlsx?)"',c.text); print("HHLINKS",c.status_code,links[:4])
if links:
    u=links[0] if links[0].startswith("http") else "https://www.ons.gov.uk"+links[0]
    x=pd.ExcelFile(io.BytesIO(s.get(u,timeout=120).content)); print("SHEETS",x.sheet_names)
    for sh in x.sheet_names:
        d=pd.read_excel(x,sh,header=None)
        m=d.astype(str).apply(lambda r: r.str.contains(r"^(England|Wales|Scotland|Great Britain|United Kingdom|UK|GB)$").any(),axis=1)
        if m.any():
            print("--- SHEET",sh,d.shape); print(d.head(12).to_string()); print(d[m].head(12).to_string())
# 1794158374
