import requests, io
import pandas as pd
pd.set_option("display.width",400); pd.set_option("display.max_columns",40); pd.set_option("display.max_colwidth",50); pd.set_option("display.max_rows",400)
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
A="https://assets.publishing.service.gov.uk/media/"
x=pd.ExcelFile(io.BytesIO(s.get(A+"69ccdb9ab50f8f8dfb8559b3/2025-provisional-greenhouse-gas-emissions-statistics-data-tables.xlsx",timeout=180).content))
print("##### PROV",x.sheet_names)
for sh in x.sheet_names:
    d=pd.read_excel(x,sh,header=None).dropna(how="all",axis=1).dropna(how="all")
    if d.shape[1]>8: d=pd.concat([d.iloc[:,:2],d.iloc[:,-4:]],axis=1)
    print("=====",sh,d.shape); print(d.head(45).to_string()[:5000])
x=pd.ExcelFile(io.BytesIO(s.get(A+"6a3bacc7eaee00074150f326/2005-24-uk-local-authority-ghg-emissions.xlsx",timeout=300).content))
print("##### LA",x.sheet_names)
for sh in x.sheet_names:
    d=pd.read_excel(x,sh,header=None)
    print("=====",sh,d.shape); print(d.head(8).to_string()[:2500])
    m=d[d.astype(str).apply(lambda r: r.str.fullmatch(r"(England|Scotland|Wales|Northern Ireland|Unallocated.*|National Total|UK|United Kingdom)").any(),axis=1)]
    if len(m): print("--- nation rows"); print(m.tail(30).to_string()[:9000])
# 1794166431
