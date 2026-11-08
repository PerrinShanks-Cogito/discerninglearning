import requests, io
import pandas as pd
pd.set_option("display.width",250); pd.set_option("display.max_columns",20)
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
h=pd.ExcelFile(io.BytesIO(s.get("https://www.ons.gov.uk/file?uri=/peoplepopulationandcommunity/healthandsocialcare/healthandlifeexpectancies/datasets/healthstatelifeexpectancyallagesuk/current/healthylifeexpectancyuk.xlsx",timeout=120).content))
d=pd.read_excel(h,"1",header=6)
print(d["Area type"].unique())
sub=d[(d["Period"]=="2022 to 2024")&(d["Area name"].isin(["United Kingdom","England","Wales","Scotland","Northern Ireland"]))&(d["Age code"].astype(str)=="1")]
print(sub[["Period","Area type","Area name","Sex","Age group","HLE","LCI","UCI","Proportion (%)"]].to_string())
# 1794156338
