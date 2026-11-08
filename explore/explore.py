import requests, io
import pandas as pd
pd.set_option("display.width",250); pd.set_option("display.max_columns",20); pd.set_option("display.max_colwidth",30)
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
u="https://www.ons.gov.uk/file?uri=/peoplepopulationandcommunity/birthsdeathsandmarriages/families/datasets/householdsbyhouseholdsizeregionsofenglandandgbconstituentcountries/2025/householdsizebyregionscountries2025.xlsx"
x=pd.ExcelFile(io.BytesIO(s.get(u,timeout=120).content))
for sh in ["England","Wales","Scotland"]:
    d=pd.read_excel(x,sh,header=None)
    print("--- ",sh,d.shape); print(d.head(9).to_string()); print(d.tail(4).to_string())
# 1794158417
