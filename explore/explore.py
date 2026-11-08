import requests, io, re
import pandas as pd
pd.set_option("display.width",320); pd.set_option("display.max_columns",30); pd.set_option("display.max_colwidth",45)
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
def get(u): r=s.get(u,timeout=180); print("GET",u[:150],r.status_code,len(r.content)); return r
# FTSE factsheet: full text of first pages
import pdfplumber
r=get("https://research.ftserussell.com/Analytics/FactSheets/Home/DownloadSingleIssue?issueName=UKX&IsManual=false")
with pdfplumber.open(io.BytesIO(r.content)) as pdf:
    for n,p in enumerate(pdf.pages[:3]):
        t=p.extract_text() or ""
        i=t.find("Constituent")
        if i>=0: print("=== page",n); print(t[max(0,i-200):i+1600])
# NI annual pay 2025
r=get("https://www.nomisweb.co.uk/api/v01/dataset/NM_30_1.data.csv?geography=N92000002,K02000001&date=latest&sex=7&item=2&pay=7&measures=20100&select=date_name,geography_name,obs_value")
print(r.text)
# regional GDP 1998-2024 related data
t=get("https://www.ons.gov.uk/economy/grossdomesticproductgdp/bulletins/regionaleconomicactivitybygrossdomesticproductuk/1998to2024/relateddata").text
ds=sorted(set(re.findall(r'href="(/economy/[^"]*/datasets/[^"]+)"',t)))
for d in ds: print("DS",d)
for d in ds:
    if not re.search(r'industry|grossdomesticproductall',d): continue
    pg=get("https://www.ons.gov.uk"+d).text
    xl=[l for l in re.findall(r'href="([^"]+\.xlsx)"',pg)]
    print("  files",xl[:3])
    if not xl: continue
    u="https://www.ons.gov.uk"+xl[0].replace("&amp;","&")
    x=pd.ExcelFile(io.BytesIO(get(u).content)); print("  sheets",x.sheet_names[:25])
    for sh in x.sheet_names:
        if sh.lower() in ("cover","contents","notes","information"): continue
        d0=pd.read_excel(x,sh,header=None,nrows=6); print("  ---",sh); print(d0.iloc[:6,:8].to_string()[:1200])
        break
# 1794174764
