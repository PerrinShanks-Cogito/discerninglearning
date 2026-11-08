import requests, io, re
import pandas as pd
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
j=s.get("https://www.gov.uk/api/content/government/statistics/offender-management-statistics-quarterly-april-to-june-2026",timeout=60).json()
att=j.get("details",{}).get("attachments",[])
for a in att: print("ATT",a.get("title"),"|",a.get("url"))
for a in att:
    u=a.get("url") or ""
    if "population" in (a.get("title") or "").lower() and u.endswith((".xlsx",".ods")):
        x=pd.ExcelFile(io.BytesIO(s.get(u,timeout=300).content))
        print("#####",u,x.sheet_names)
        for sh in x.sheet_names:
            if re.search(r"1\.?Q\.?7|ethnic",sh,re.I) or sh.startswith("1_Q_7") or sh in ("Table_1_Q_7","1.Q.7"):
                d=pd.read_excel(x,sh,header=None).dropna(how="all",axis=1).dropna(how="all")
                print("=====",sh); print(d.to_string(max_colwidth=40)[:6000])
for p in ["https://www.justice-ni.gov.uk/node/421705","https://www.justice-ni.gov.uk/node/421708"]:
    try:
        t=s.get(p,timeout=60).text; t=re.sub(r"<[^>]+>"," ",t); t=re.sub(r"\s+"," ",t)
        for m in re.finditer(r"[^.]{0,200}(reoffend|re-offend)[^.]{0,200}\.",t): print("NI:",m.group(0)[:400])
    except Exception as e: print("ERR",p,e)
# 1794168948
# 1794170181
# 1794170798
