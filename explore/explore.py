import requests, io
import pandas as pd
pd.set_option("display.width",400); pd.set_option("display.max_columns",40); pd.set_option("display.max_colwidth",60); pd.set_option("display.max_rows",300)
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
A="https://assets.publishing.service.gov.uk/media/"
def X(u): return pd.ExcelFile(io.BytesIO(s.get(u,timeout=180).content))
x=X(A+"6a69f47e701b2d693e5b9420/DUKES_4.1.1.xlsx"); d=pd.read_excel(x,"Methane",header=None)
print(list(enumerate(d.iloc[5].tolist()))); print(d.iloc[[59,60,61]].to_string())
x=X(A+"6aba96a9734e2435f202f1d6/DUKES_4.5.xlsx"); d=pd.read_excel(x,"4.5a",header=None).dropna(how="all",axis=1)
print(list(d.iloc[5])); print(pd.concat([d.iloc[5:,:4],d.iloc[5:,-2:]],axis=1).to_string())
# 1794165628
