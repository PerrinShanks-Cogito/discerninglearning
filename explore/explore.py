import requests, io, zipfile, pandas as pd
pd.set_option("display.width",250)
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (landmark-numbers)"})
z=zipfile.ZipFile(io.BytesIO(s.get("https://www.england.nhs.uk/wp-content/uploads/2026/10/NCC_FY2025-26_Org_File1.zip",timeout=600).content))
df=pd.read_csv(z.open(z.namelist()[0]),encoding="utf-8-sig",low_memory=False,dtype=str)
print(df.head(3).to_string())
a=pd.to_numeric(df["Activity"],errors="coerce"); c=pd.to_numeric(df["Actual Cost"],errors="coerce")
bad=df[a.isna()|c.isna()]
print("rows",len(df),"bad",len(bad)); print(bad.head(20).to_string())
print(bad["Activity"].value_counts().head(10)); print(bad["Actual Cost"].value_counts().head(10))
print(bad.assign(c=pd.to_numeric(bad["Actual Cost"],errors="coerce")).groupby("Department Code")["c"].agg(["count","sum"]).to_string())
el=df[df["Department Code"]=="EL"].assign(a=a,c=c)
print(el.groupby("Currency Code")[["a","c"]].sum().sort_values("c",ascending=False).head(10))
print("total cost all rows",c.sum()/1e9,"valid rows",c[a.notna()].sum()/1e9)
