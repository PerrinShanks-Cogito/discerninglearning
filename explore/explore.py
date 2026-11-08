import requests, re, io, html, traceback
import pandas as pd
pd.set_option("display.width",250); pd.set_option("display.max_columns",30); pd.set_option("display.max_colwidth",50)
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
def links(u, pat):
    r=s.get(u,timeout=90); return r.status_code, [l if l.startswith("http") else ("https://www.ons.gov.uk"+l if "ons.gov.uk" in u else l) for l in re.findall(r'href="([^"]+)"',r.text) if re.search(pat,l,re.I)]
def sec(name):
    print("\n#########",name)
# a) mid-2025 components of change
sec("MYE components")
try:
    c,l=links("https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/datasets/populationestimatesforukenglandandwalesscotlandandnorthernireland",r"\.xlsx?$")
    print(c,l[:3])
    x=pd.ExcelFile(io.BytesIO(s.get(l[0],timeout=180).content)); print(x.sheet_names)
    for sh in x.sheet_names:
        if re.search(r"MYE3|component",sh,re.I):
            d=pd.read_excel(x,sh,header=None); print("--",sh,d.shape); 
            hi=next(i for i in range(15) if d.iloc[i].astype(str).str.contains("Code|code").any())
            d.columns=d.iloc[hi]; d=d.iloc[hi+1:]
            print(list(d.columns))
            print(d[d.iloc[:,1].astype(str).str.fullmatch("UNITED KINGDOM|ENGLAND|WALES|SCOTLAND|NORTHERN IRELAND|United Kingdom|England|Wales|Scotland|Northern Ireland")].to_string())
except Exception: traceback.print_exc()
# b) Census 2021 religion E&W via Nomis TS030
sec("TS030")
try:
    r=s.get("https://www.nomisweb.co.uk/api/v01/dataset/NM_2049_1.data.csv?geography=2092957699,2092957700&measures=20100,20301&select=geography_name,c2021_religion_10_name,measures_name,obs_value",timeout=90)
    print(r.status_code); print(r.text[:3000])
except Exception: traceback.print_exc()
# c) NISRA religion
sec("NISRA")
try:
    c,l=links("https://www.nisra.gov.uk/publications/census-2021-main-statistics-religion-tables",r"\.xlsx?$")
    print(c,l)
    for u in l:
        if re.search(r"ms-b19|b19",u,re.I):
            x=pd.ExcelFile(io.BytesIO(s.get(u,timeout=120).content)); print(x.sheet_names)
            for sh in x.sheet_names[:4]:
                d=pd.read_excel(x,sh,header=None); print("--",sh,d.shape); print(d.head(12).to_string())
except Exception: traceback.print_exc()
# d) DWP UC statistics page attachments + NI DfC
sec("UC")
try:
    c,l=links("https://www.gov.uk/government/collections/universal-credit-statistics",r"universal-credit-statistics-29-april-2013")
    print(c,l[:6])
    if l:
        u=l[0] if l[0].startswith("http") else "https://www.gov.uk"+l[0]
        r=s.get(u,timeout=90); t=html.unescape(re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",r.text)))
        print(u); 
        for m in re.finditer(r"[^.]{0,200}(Scotland|Wales|England|region)[^.]{0,250}\.",t): print("  ",m.group(0)[:400])
        print([a for a in re.findall(r'href="([^"]+)"',r.text) if re.search(r"\.(ods|xlsx|csv)$",a)])
except Exception: traceback.print_exc()
try:
    r=s.get("https://www.communities-ni.gov.uk/topics/benefits-statistics/universal-credit-statistics",timeout=90)
    t=html.unescape(re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",r.text))); print("DFC",r.status_code)
    print([a for a in re.findall(r'href="([^"]+)"',r.text) if re.search(r"universal-credit",a)][:15])
except Exception: traceback.print_exc()
# e) CRA social protection per head
sec("CRA social protection")
try:
    x=pd.ExcelFile(io.BytesIO(s.get("https://assets.publishing.service.gov.uk/media/691b0990d140bbbaa59a28ad/CRA_2025_Chapter_A_tables.xlsx",timeout=120).content))
    df=pd.read_excel(x,"A.15",header=None)
    hdr=df.iloc[2].tolist(); cols={str(v).strip():i for i,v in enumerate(hdr)}
    want=[k for k in cols if re.match(r"^(2\. Defence|10\. Social protection|7\. Health|Total)",k)]
    year=None
    for i,r in df.iterrows():
        v=str(r[0]).strip()
        if re.match(r"^20\d\d-\d\d",v): year=v
        if year=="2024-25" and v in ("England","Scotland","Wales","Northern Ireland","UK identifiable expenditure"):
            print(year,v,{k:r[cols[k]] for k in want})
except Exception: traceback.print_exc()
# 1794158742
