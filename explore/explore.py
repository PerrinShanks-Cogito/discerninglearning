import requests, io, re, json
import pandas as pd
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
def get(u,**k):
    r=s.get(u,timeout=120,**k); print("GET",u[:140],r.status_code,len(r.content)); return r
# A. ONS GDP time series
for cdid,ds in [("ybha","ukea"),("abmi","ukea"),("ihyp","ukea")]:
    try:
        j=get(f"https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/{cdid}/{ds}/data").json()
        print(cdid, j["description"]["title"], j["description"].get("releaseDate"), [(y["year"],y["value"]) for y in j["years"][-4:]])
    except Exception as e: print("ERR",cdid,e)
# B/C. dataset pages -> xlsx links
for page in ["https://www.ons.gov.uk/economy/grossdomesticproductgdp/datasets/regionalgrossvalueaddedbalancedbyindustryandallinternationalterritoriallevelsitlregions",
             "https://www.ons.gov.uk/economy/grossdomesticproductgdp/datasets/regionalgrossdomesticproductallnutslevelregions",
             "https://www.ons.gov.uk/economy/grossdomesticproductgdp/datasets/regionalgrossdomesticproductallitlregions"]:
    try:
        t=get(page).text
        print("PAGE",page.split('/')[-1], re.findall(r'Release date:\s*</span>\s*([^<]+)',t)[:1])
        for l in sorted(set(re.findall(r'href="([^"]+\.xlsx)"',t)))[:6]: print("   ",l)
    except Exception as e: print("ERR",page,e)
# D. Nomis ASHE definitions and data
for d in ["sex","item","pay"]:
    try:
        j=get(f"https://www.nomisweb.co.uk/api/v01/dataset/NM_30_1/{d}.def.sjson").json()
        print(d,[(c["value"],c["description"]["value"]) for c in j["structure"]["codelists"]["codelist"][0]["code"]][:12])
    except Exception as e: print("ERR",d,e)
try:
    r=get("https://www.nomisweb.co.uk/api/v01/dataset/NM_30_1.data.csv?geography=K02000001,E92000001,W92000004,S92000003,N92000002&date=latestMINUS1,latest&sex=7,8&item=2&pay=1,7&measures=20100&select=date_name,geography_name,sex_name,pay_name,obs_value,obs_status_name")
    print(r.text[:3000])
except Exception as e: print("ERR nomis",e)
# E. FTSE 100 factsheet
for u in ["https://research.ftserussell.com/Analytics/FactSheets/Home/DownloadSingleIssue?issueName=UKX&IsManual=false",
          "https://research.ftserussell.com/Analytics/FactSheets/temp/ukx.pdf"]:
    try:
        r=get(u)
        if r.content[:4]==b"%PDF":
            import pdfplumber
            with pdfplumber.open(io.BytesIO(r.content)) as pdf:
                txt="\n".join(p.extract_text() or "" for p in pdf.pages[:3])
            i=txt.find("Top 10"); print("FACTSHEET", txt[:300].replace("\n"," | ")); print(txt[i:i+1500])
            break
    except Exception as e: print("ERR ftse",e)
# 1794174702
