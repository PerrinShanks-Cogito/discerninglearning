import requests, re, io, html, traceback
import pandas as pd
pd.set_option("display.width",250); pd.set_option("display.max_columns",40); pd.set_option("display.max_colwidth",40)
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
txt=lambda h: html.unescape(re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",re.sub(r"(?s)<(script|style).*?</\1>","",h))))
print("######### Claimant count")
try:
    r=s.get("https://www.nomisweb.co.uk/api/v01/dataset/NM_162_1.data.csv?geography=TYPE499&date=latest&gender=0&age=0&measure=1,2&measures=20100&select=date_name,geography_name,measure_name,obs_value",timeout=90)
    print(r.status_code); print(r.text[:1500])
except Exception: traceback.print_exc()
print("######### NI UC May 2026")
try:
    r=s.get("https://www.communities-ni.gov.uk/publications/universal-credit-statistics-may-2026",timeout=90); t=txt(r.text); print(r.status_code)
    for m in re.finditer(r"[^.]{0,250}(people|claimants|households)[^.]{0,250}\.",t):
        if re.search(r"\d",m.group(0)): print("  ",m.group(0)[:400])
    print([a for a in re.findall(r'href="([^"]+)"',r.text) if re.search(r"\.(pdf|xlsx|ods|csv)",a)][:5])
except Exception: traceback.print_exc()
print("######### GB UC May 2026 headline")
try:
    r=s.get("https://www.gov.uk/government/statistics/universal-credit-quarterly-statistics-29-april-2013-to-14-may-2026/universal-credit-quarterly-statistics-29-april-2013-to-14-may-2026",timeout=90); t=txt(r.text)
    for m in re.finditer(r"[^.]{0,200}(8\.\d million|people on Universal Credit)[^.]{0,200}\.",t): print("  ",m.group(0)[:400])
except Exception: traceback.print_exc()
print("######### NI MS-B20")
try:
    x=pd.ExcelFile(io.BytesIO(s.get("https://www.nisra.gov.uk/system/files/statistics/census-2021-ms-b20.xlsx",timeout=120).content))
    d=pd.read_excel(x,"NI",header=None); print(d.iloc[7:11].T.to_string())
except Exception: traceback.print_exc()
print("######### Scotland religion")
try:
    r=s.get("https://www.scotlandscensus.gov.uk/2022-results/scotland-s-census-2022-ethnic-group-national-identity-language-and-religion",timeout=90)
    ls=[a for a in re.findall(r'href="([^"]+)"',r.text) if re.search(r"\.(xlsx|csv|ods|zip)|religion|UV205|data",a,re.I)]
    print(ls[:30])
    for a in ls:
        if re.search(r"\.(xlsx|csv|ods)$",a,re.I):
            u=a if a.startswith("http") else "https://www.scotlandscensus.gov.uk"+a
            b=s.get(u,timeout=120).content
            try:
                x=pd.ExcelFile(io.BytesIO(b)); print("FILE",u,x.sheet_names[:12])
                for sh in x.sheet_names:
                    d=pd.read_excel(x,sh,header=None)
                    m=d.astype(str).apply(lambda r: r.str.contains("Sikh|Hindu").any(),axis=1)
                    if m.any(): print("--",sh); print(d.head(30).to_string()[:4000]); break
            except Exception as e: print("ERRFILE",u,e)
except Exception: traceback.print_exc()
# 1794158860
