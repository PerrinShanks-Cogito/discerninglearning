import requests, re, io, zipfile
from bs4 import BeautifulSoup
import pandas as pd
H={"User-Agent":"Mozilla/5.0 (landmark-numbers bot)"}
url="https://www.england.nhs.uk/publication/2024-25-national-cost-collection-data-publication/"
r=requests.get(url,headers=H,timeout=60); print("STATUS",r.status_code)
s=BeautifulSoup(r.text,"html.parser")
main=s.find("main") or s
print("TEXT:", main.get_text(" ",strip=True)[:3000])
links=[(a.get_text(strip=True),a["href"]) for a in s.find_all("a",href=True) if re.search(r"\.(xlsx|xls|zip|csv|pdf)$",a["href"],re.I)]
for t,h in links: print("LINK",t,"|",h)
for t,h in links:
    if not re.search(r"\.(xlsx|xls)$",h,re.I): 
        if h.lower().endswith(".zip"):
            try:
                z=requests.get(h,headers=H,timeout=300); print("ZIP",h,len(z.content))
                zf=zipfile.ZipFile(io.BytesIO(z.content))
                for n in zf.infolist()[:50]: print("  ZIPENTRY",n.filename,n.file_size)
            except Exception as e: print("ZIPERR",e)
        continue
    try:
        b=requests.get(h,headers=H,timeout=300).content
        print("\n=== FILE",t,h,len(b))
        x=pd.ExcelFile(io.BytesIO(b))
        for sh in x.sheet_names:
            df=x.parse(sh,header=None,nrows=25)
            print("--- SHEET",sh, x.book[sh].max_row if hasattr(x,'book') else "")
            print(df.iloc[:25,:12].to_string(max_colwidth=40))
    except Exception as e: print("ERR",h,e)
