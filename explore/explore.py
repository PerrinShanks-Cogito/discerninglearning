import requests, io, zipfile, re, pandas as pd
pd.set_option("display.width",250)
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (landmark-numbers)"})
z=zipfile.ZipFile(io.BytesIO(s.get("https://www.england.nhs.uk/wp-content/uploads/2026/10/NCC_FY2025-26_NCCI.zip",timeout=600).content))
n=[x for x in z.namelist() if "Department and Service Unadjusted" in x][0]
df=pd.read_csv(z.open(n),encoding="utf-8-sig",dtype=str)
print(df.shape); print(df.head(3).to_string())
num=lambda s: pd.to_numeric(s.str.replace(r"[£,Â\s]","",regex=True),errors="coerce")
df["a"]=num(df["Activity"]); df["c"]=num(df["Actual Cost"])
print("suppressed act",df["a"].isna().sum(),"cost",df["c"].isna().sum()); print(df.loc[df["a"].isna(),"Activity"].value_counts().head())
print(df["Department"].value_counts().to_string())
print("total £bn",df["c"].sum()/1e9)
df["code"]=df["Provider"].str.split(" - ").str[0]
g=df.groupby("Department")[["a","c"]].sum(); g["u"]=g.c/g.a
r=df[df.code=="RJ1"].groupby("Department")[["a","c"]].sum(); r["u"]=r.c/r.a
print(g.join(r,rsuffix="_RJ1").to_string())
print(df[df.Service.str.startswith("01EC")].groupby("Service")[["a","c"]].sum().assign(u=lambda t:t.c/t.a))
print(df[(df.code=="RJ1")&df.Service.str.contains("EC")][["Service","Department","a","c","Unit Cost","NCCI"]].to_string())
print("RJ1 total",df.loc[df.code=="RJ1","c"].sum()/1e9)
