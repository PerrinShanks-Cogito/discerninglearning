import requests, io, re, html
import pandas as pd
pd.set_option("display.width",250); pd.set_option("display.max_columns",40)
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
u="https://www.ons.gov.uk/file?uri=/peoplepopulationandcommunity/birthsdeathsandmarriages/families/datasets/householdsbyhouseholdsizeregionsofenglandandgbconstituentcountries/2025/householdsizebyregionscountries2025.xlsx"
x=pd.ExcelFile(io.BytesIO(s.get(u,timeout=120).content))
d=pd.read_excel(x,"England",header=None); print(d.iloc[9:13,:8].to_string())
for p in ["https://www.nisra.gov.uk/statistics/population/household-projections","https://www.nisra.gov.uk/publications/ct0078-households"]:
    r=s.get(p,timeout=60); t=html.unescape(re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",re.sub(r"(?s)<(script|style).*?</\1>","",r.text))))
    print("NISRA",p,r.status_code)
    for m in re.finditer(r"[^.]{0,200}\b(households?)\b[^.]{0,200}\.",t):
        if re.search(r"\d{3},\d{3}|\d+(\.\d)? million|20(2[0-9]|3[0-9])",m.group(0)): print("   ",m.group(0)[:400])
# 1794158470
