import requests, io, re
import pandas as pd
pd.set_option("display.width",300); pd.set_option("display.max_columns",40); pd.set_option("display.max_colwidth",40); pd.set_option("display.max_rows",200)
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
pages=["/government/statistics/electricity-chapter-5-digest-of-united-kingdom-energy-statistics-dukes",
"/government/statistics/renewable-sources-of-energy-chapter-6-digest-of-united-kingdom-energy-statistics-dukes",
"/government/statistics/energy-trends-september-2026-special-feature-article-electricity-generation-and-supply-in-scotland-wales-northern-ireland-and-england-2021-to-2025",
"/government/statistics/energy-trends-section-5-electricity",
"/government/statistics/energy-trends-section-6-renewables",
"/government/publications/interconnectors-electricity"]
for p in pages:
    try:
        j=s.get("https://www.gov.uk/api/content"+p,timeout=60).json()
        print("#####",p,j.get("public_updated_at"))
        for a in j.get("details",{}).get("attachments",[]):
            print("  ",a.get("title"),"|",a.get("url"))
    except Exception as e: print("ERR",p,e)
# 1794165359
