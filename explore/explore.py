import requests, re, io, html, traceback
import pandas as pd
pd.set_option("display.width",250); pd.set_option("display.max_columns",30); pd.set_option("display.max_colwidth",50)
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
txt=lambda h: html.unescape(re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",re.sub(r"(?s)<(script|style).*?</\1>","",h))))
print("######### NISRA B19")
try:
    x=pd.ExcelFile(io.BytesIO(s.get("https://www.nisra.gov.uk/system/files/statistics/census-2021-ms-b19.xlsx",timeout=120).content)); print(x.sheet_names)
    for sh in x.sheet_names:
        d=pd.read_excel(x,sh,header=None)
        m=d.astype(str).apply(lambda r: r.str.contains("Northern Ireland").any(),axis=1)
        if m.any() and d.shape[1]>4:
            print("--",sh,d.shape); print(d.head(10).to_string()); print(d[m].head(3).to_string())
except Exception: traceback.print_exc()
print("######### UC release")
try:
    r=s.get("https://www.gov.uk/government/collections/universal-credit-statistics",timeout=90)
    rel=[l for l in re.findall(r'href="(/government/statistics/universal-credit-statistics-29-april-2013-to-[^"]+)"',r.text) if "announcements" not in l]
    print(rel[:5])
    u="https://www.gov.uk"+rel[0]; r=s.get(u,timeout=90); print(u)
    sub=[l for l in re.findall(r'href="(/government/statistics/universal-credit-statistics[^"]+/universal-credit-statistics[^"]+)"',r.text)]
    print(sub[:3])
    if sub:
        r2=s.get("https://www.gov.uk"+sub[0],timeout=90); t=txt(r2.text)
        for m in re.finditer(r"[^.]{0,250}(Scotland|Wales|Northern Ireland|country|countries)[^.]{0,250}\.",t): print("  ",m.group(0)[:450])
        i=t.find("people on Universal Credit"); print("HEAD",t[i-300:i+600])
    print([a for a in re.findall(r'href="([^"]+)"',r.text) if re.search(r"\.(ods|xlsx|csv)",a)])
except Exception: traceback.print_exc()
print("######### DfC UC")
try:
    for u in ["https://www.communities-ni.gov.uk/articles/universal-credit-statistics","https://www.communities-ni.gov.uk/topics/universal-credit-statistics","https://www.communities-ni.gov.uk/publications/topic/8182"]:
        r=s.get(u,timeout=60); print(u,r.status_code)
        if r.status_code==200:
            print([a for a in re.findall(r'href="([^"]+)"',r.text) if re.search(r"universal-credit-statistics",a,re.I)][:10])
except Exception: traceback.print_exc()
# 1794158799
