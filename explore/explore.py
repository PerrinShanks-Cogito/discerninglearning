import requests, re, io, traceback
import pandas as pd
pd.set_option("display.width",300); pd.set_option("display.max_columns",30); pd.set_option("display.max_colwidth",60); pd.set_option("display.max_rows",400)
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
try:
    r=s.get("https://www.gov.uk/government/statistics/uk-armed-forces-equipment-and-formations-2026",timeout=90)
    ls=sorted(set(a for a in re.findall(r'href="([^"]+)"',r.text) if re.search(r"\.(ods|xlsx|csv)$",a))); print(ls)
    for u in ls:
        b=s.get(u,timeout=180).content
        x=pd.ExcelFile(io.BytesIO(b),engine="odf" if u.endswith(".ods") else None); print("FILE",u,x.sheet_names)
        for sh in x.sheet_names:
            d=pd.read_excel(x,sh,header=None)
            txt=d.astype(str)
            hit=txt.apply(lambda r: r.str.contains(r"F-35|Lightning|Challenger|Type 45|Type 23|Type 26|Queen Elizabeth|Carrier|Destroyer|Frigate|Astute|Vanguard|Apache|Wildcat|Merlin|A400M|Voyager|C-17|Poseidon|P-8|Archer|AS90|MLRS|Boxer|Ajax|Typhoon|Chinook",case=False).any(),axis=1)
            if hit.any():
                print("--",sh,d.shape)
                sub=d[hit]
                # print label col(s) and last non-null value
                for i,row in sub.iterrows():
                    vals=[v for v in row.tolist() if pd.notna(v)]
                    print("   ",[str(v)[:45] for v in vals][:12])
except Exception: traceback.print_exc()
# 1794164839
