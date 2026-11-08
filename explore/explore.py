import requests, re, io, html, json
import pandas as pd
pd.set_option("display.width",250); pd.set_option("display.max_columns",30)
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
def text(u):
    r=s.get(u,timeout=90); return r.status_code, html.unescape(re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",re.sub(r"(?s)<(script|style).*?</\1>","",r.text)))), r.text
N="https://www.nomisweb.co.uk/api/v01/dataset/"
# 1. ASHE median full-time gross weekly pay, residence (NM_30_1) and workplace (NM_99_1), UK countries
for ds in ["NM_30_1","NM_99_1"]:
    for q in [f"{N}{ds}.data.csv?geography=TYPE499&date=latest&sex=8&item=2&pay=1&measures=20100&select=date_name,geography_name,geography_code,sex_name,item_name,pay_name,obs_value",
              f"{N}{ds}.data.csv?geography=TYPE499&date=latest&sex=7&item=2&pay=1&measures=20100&select=date_name,geography_name,geography_code,sex_name,item_name,pay_name,obs_value"]:
        r=s.get(q,timeout=90); print("NOMIS",ds,r.status_code); print(r.text[:900])
# 1b. check UK geography code
r=s.get(f"{N}NM_30_1/geography/TYPE499.def.sdmx.json",timeout=90); print("GEO",r.status_code,r.text[:1500])
# 2. Regional labour market, latest bulletins
for m in ["november2026","october2026"]:
    c,t,_=text(f"https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/bulletins/regionallabourmarket/{m}")
    print("LM",m,c)
    for x in re.finditer(r"[^.]{0,250}employment rate[^.]{0,300}\.",t): print("  ",x.group(0)[:500])
# 3. HLE datasets: related data links
c,t,raw=text("https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthandlifeexpectancies/bulletins/healthstatelifeexpectanciesuk/between2011to2013and2022to2024/relateddata")
print("HLEREL",c); print([l for l in set(re.findall(r'href="([^"]+)"',raw)) if "dataset" in l][:20])
# 4. CRA 2025 attachments
c,t,raw=text("https://www.gov.uk/government/statistics/country-and-regional-analysis-2025")
print("CRA",c); print([l for l in set(re.findall(r'href="([^"]+)"',raw)) if re.search(r"\.(xlsx|ods|csv)$",l)])
c,t,raw=text("https://www.gov.uk/government/statistics/country-and-regional-analysis-2025/country-and-regional-analysis-november-2025")
for x in re.finditer(r"[^.]{0,200}[Hh]ealth[^.]{0,300}\.",t): print("CRAH",x.group(0)[:400])
print([l for l in set(re.findall(r'href="([^"]+)"',raw)) if re.search(r"\.(xlsx|ods|csv)$",l)])
# 1794156163
