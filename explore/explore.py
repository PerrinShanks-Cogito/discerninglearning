import requests
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
for p in ["/government/statistics/provisional-uk-greenhouse-gas-emissions-statistics-2025","/government/statistics/final-uk-greenhouse-gas-emissions-national-statistics-1990-to-2024","/government/statistics/uk-local-authority-and-regional-greenhouse-gas-emissions-statistics-2005-to-2024"]:
    try:
        j=s.get("https://www.gov.uk/api/content"+p,timeout=60).json(); print("#####",p,j.get("public_updated_at"))
        for a in j.get("details",{}).get("attachments",[]): print("  ",a.get("title"),"|",a.get("url"))
    except Exception as e: print("ERR",p,e)
import re
for u in ["https://naei.energysecurity.gov.uk/reports/greenhouse-gas-inventories-england-scotland-wales-and-northern-ireland-1990-2024","https://naei.energysecurity.gov.uk/data/data-selector"]:
    try:
        t=s.get(u,timeout=60).text; print("#####",u,len(t))
        for l in sorted(set(re.findall(r'href="([^"]+\.(?:xlsx|xls|csv|ods|pdf|zip))"',t))): print("  ",l)
    except Exception as e: print("ERR",u,e)
# 1794166393
