import requests, io, zipfile, pandas as pd
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (landmark-numbers)"})
base="https://www.england.nhs.uk/wp-content/uploads/2026/10/"
for f in ["NCC_FY2025-26_National_Schedule.zip","NCC_FY2025-26_NCCI.zip","NCC_FY2025-26_Org_File3.zip","NCC_FY2025-26_Org_File1.zip"]:
    b=s.get(base+f,timeout=600).content
    z=zipfile.ZipFile(io.BytesIO(b)); print("\n######",f,len(b))
    for n in z.infolist():
        print("ENTRY",n.filename,n.file_size)
        data=z.read(n)
        if n.filename.lower().endswith((".xlsx",".xlsb",".xls")):
            try:
                x=pd.ExcelFile(io.BytesIO(data))
                for sh in x.sheet_names:
                    df=x.parse(sh,header=None,nrows=14)
                    print("--- SHEET",sh); print(df.iloc[:14,:10].to_string(max_colwidth=32))
            except Exception as e: print("XERR",e)
        elif n.filename.lower().endswith((".csv",".txt")):
            lines=data[:200000].decode("latin-1").splitlines()
            print("HEAD"); print("\n".join(lines[:4]))
            rj=[l for l in lines if "RJ1" in l][:3]; print("RJ1 sample",rj)
