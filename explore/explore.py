import requests, io, zipfile, pandas as pd
pd.set_option("display.width",250); pd.set_option("display.max_rows",500)
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (landmark-numbers)"})
base="https://www.england.nhs.uk/wp-content/uploads/2026/10/"
def z(f): return zipfile.ZipFile(io.BytesIO(s.get(base+f,timeout=600).content))
z3=z("NCC_FY2025-26_Org_File3.zip")
dd=pd.read_excel(io.BytesIO(z3.read("NCC_FY2025-26_Org_File3/Department Description.xlsx")))
print(dd.to_string())
org=pd.read_excel(io.BytesIO(z3.read("NCC_FY2025-26_Org_File3/Organisation Description.xlsx")))
print(org.columns.tolist()); print(org[org.iloc[:,0].astype(str).str.startswith(("RJ1","RJZ","R1H","RYJ","RRV"))].to_string())
frames=[]
for f in ["NCC_FY2025-26_Org_File1.zip","NCC_FY2025-26_Org_File2.zip"]:
    zz=z(f)
    for n in zz.namelist():
        if n.endswith(".csv"):
            df=pd.read_csv(zz.open(n),encoding="utf-8-sig",low_memory=False); print(f,n,df.shape,df.columns.tolist()); frames.append(df)
d=pd.concat(frames)
d["Activity"]=pd.to_numeric(d["Activity"],errors="coerce"); d["Actual Cost"]=pd.to_numeric(d["Actual Cost"],errors="coerce")
print("TOTAL national cost £bn",d["Actual Cost"].sum()/1e9, "providers",d["Provider Code"].nunique())
g=d.groupby("Department Code")[["Activity","Actual Cost"]].sum(); g["unit"]=g["Actual Cost"]/g["Activity"]
r=d[d["Provider Code"]=="RJ1"].groupby("Department Code")[["Activity","Actual Cost"]].sum(); r["unit"]=r["Actual Cost"]/r["Activity"]
print(g.join(r,rsuffix="_RJ1").to_string())
print("RJ1 total £bn",d.loc[d["Provider Code"]=="RJ1","Actual Cost"].sum()/1e9)
for dep in ["EM","EC","AE"]:
    x=d[d["Department Code"]==dep]
    if len(x):
        print("DEPT",dep); print(x.groupby("Service Code")[["Activity","Actual Cost"]].sum().assign(u=lambda t:t["Actual Cost"]/t["Activity"]).to_string())
        print(x[x["Provider Code"]=="RJ1"].groupby("Service Code")[["Activity","Actual Cost"]].sum().assign(u=lambda t:t["Actual Cost"]/t["Activity"]).to_string())
zn=z("NCC_FY2025-26_NCCI.zip")
m=pd.read_excel(io.BytesIO(zn.read("NCC_FY2025-26_NCCI/NCCI by Mapping Pot MFF Adjusted.xlsx")),header=None)
print(m.iloc[0].tolist()); print(m[m[0].astype(str).str.startswith(("RJ1","RJZ","R1H","RYJ","RRV"))].to_string())
