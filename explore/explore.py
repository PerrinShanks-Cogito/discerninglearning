import requests, re, io, html, traceback
import pandas as pd
pd.set_option("display.width",250); pd.set_option("display.max_columns",40); pd.set_option("display.max_colwidth",60)
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
print("######### OBR databank")
try:
    for u in ["https://obr.uk/data/","https://obr.uk/public-finances-databank/"]:
        r=s.get(u,timeout=90); print(u,r.status_code)
        ls=sorted(set(a for a in re.findall(r'href="([^"]+)"',r.text) if re.search(r"databank|public-finances",a,re.I)))
        print(ls[:20])
except Exception: traceback.print_exc()
print("######### ONS PSF appendix D")
try:
    u="https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/datasets/publicsectorfinancesappendixdtables"
    r=s.get(u,timeout=90); ls=[a for a in re.findall(r'href="([^"]+\.xlsx)"',r.text)]; print(r.status_code, ls[:3])
    if ls:
        x=pd.ExcelFile(io.BytesIO(s.get("https://www.ons.gov.uk"+ls[0],timeout=180).content)); print(x.sheet_names)
        for sh in x.sheet_names:
            if re.search(r"PSA6|receipt|6B|6C",sh,re.I):
                d=pd.read_excel(x,sh,header=None); print("--",sh,d.shape); print(d.iloc[:12,:14].to_string()[:3000])
                m=d.astype(str).apply(lambda r: r.str.contains(r"2025-26|2025/26|FYE 2026|2025-2026").any(),axis=1)
                print(d[m].iloc[:, :40].to_string()[:3000])
except Exception: traceback.print_exc()
# 1794159925
