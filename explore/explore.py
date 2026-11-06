import requests, re, json, time
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
H={"User-Agent":UA,"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language":"en-GB,en;q=0.9"}
s=requests.Session(); s.headers.update(H)
def show(u):
    for i in range(3):
        try:
            r=s.get(u,timeout=60); print("GET",u,r.status_code,len(r.content),r.headers.get("content-type"),r.headers.get("server"))
            if r.status_code==200: return r
            print("  BODY",r.text[:400].replace("\n"," ")); time.sleep(5)
        except Exception as e: print("ERR",u,e)
pub="https://www.england.nhs.uk/publication/2024-25-national-cost-collection-data-publication/"
r=show(pub)
if r is not None and r.status_code==200:
    for h in set(re.findall(r'href="([^"]+\.(?:xlsx|xls|zip|csv|pdf))"',r.text,re.I)): print("LINK",h)
for q in ["national schedule","national cost collection index","2024/25 National Cost Collection","NCC 2024"]:
    r=show("https://www.england.nhs.uk/wp-json/wp/v2/media?per_page=50&search="+requests.utils.quote(q))
    if r is not None and r.status_code==200:
        try:
            for m in r.json(): print("MEDIA",m.get("date"),m.get("source_url"))
        except Exception as e: print("JSONERR",e,r.text[:200])
