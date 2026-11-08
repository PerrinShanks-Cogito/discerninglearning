import requests, io, zipfile
import pandas as pd
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
z=zipfile.ZipFile(io.BytesIO(s.get("https://naei.energysecurity.gov.uk/sites/default/files/2026-07/NAEI24_GHG_CSV_files.zip",timeout=300).content))
for n in z.namelist(): print(n, z.getinfo(n).file_size)
for n in z.namelist():
    if n.lower().endswith(".csv"):
        d=pd.read_csv(z.open(n),nrows=3,encoding="latin1"); print("=====",n); print(list(d.columns)); print(d.head(2).to_string()[:1500])
# 1794166592
