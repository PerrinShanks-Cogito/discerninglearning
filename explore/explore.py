import requests, re, io, html, traceback
import pandas as pd
pd.set_option("display.width",250); pd.set_option("display.max_columns",40); pd.set_option("display.max_colwidth",45)
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
print("######### NI UC ods")
try:
    b=s.get("https://www.communities-ni.gov.uk/system/files/2026-08/dfc-ni-uc-stats-supp-tables-may-2026.ods",timeout=120).content
    x=pd.ExcelFile(io.BytesIO(b),engine="odf"); print(x.sheet_names[:15])
    for sh in x.sheet_names[:6]:
        d=pd.read_excel(x,sh,header=None); print("--",sh,d.shape); print(d.head(14).to_string()[:2500])
except Exception: traceback.print_exc()
print("######### Scotland chart data")
try:
    r=s.get("https://www.scotlandscensus.gov.uk/documents/scotlands-census-2022-ethnic-group-national-identity-language-and-religion-chart-data/",timeout=90)
    ls=[a for a in re.findall(r'href="([^"]+)"',r.text) if re.search(r"\.(xlsx|csv|ods)",a,re.I)]; print(ls)
    for a in ls[:2]:
        u=a if a.startswith("http") else "https://www.scotlandscensus.gov.uk"+a
        x=pd.ExcelFile(io.BytesIO(s.get(u,timeout=120).content)); print(x.sheet_names)
        for sh in x.sheet_names:
            d=pd.read_excel(x,sh,header=None)
            if d.astype(str).apply(lambda r: r.str.contains("Sikh|Hindu|No religion",case=False).any(),axis=1).any():
                print("--",sh); print(d.to_string()[:3500])
except Exception: traceback.print_exc()
print("######### NI MS-B20 sheets")
try:
    x=pd.ExcelFile(io.BytesIO(s.get("https://www.nisra.gov.uk/system/files/statistics/census-2021-ms-b20.xlsx",timeout=120).content)); print(x.sheet_names)
    for sh in x.sheet_names:
        if re.search(r"^(NI|Northern)",sh):
            d=pd.read_excel(x,sh,header=None); print(d.iloc[7:11].T.to_string())
except Exception: traceback.print_exc()
# 1794158908
