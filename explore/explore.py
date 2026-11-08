import requests, io
import pandas as pd
pd.set_option("display.width",300); pd.set_option("display.max_columns",30); pd.set_option("display.max_colwidth",50); pd.set_option("display.max_rows",100)
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
x=pd.ExcelFile(io.BytesIO(s.get("https://assets.publishing.service.gov.uk/media/6a7afefb423b0bdba0290eb1/UK_armed_forces_equipment_and_formations_2026.xlsx",timeout=180).content))
for sh in ["1","5","7","8"]:
    d=pd.read_excel(x,sh,header=None); print("=====",sh); print(d.to_string(max_colwidth=50)[:6000])
# 1794164882
