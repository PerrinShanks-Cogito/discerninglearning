import requests, re, json
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (landmark-numbers)"})
for pid in [294161,275980]:
    p=s.get(f"https://www.england.nhs.uk/wp-json/wp/v2/documents/{pid}",timeout=60).json()
    raw=json.dumps(p)
    print("\nDOC",pid,p.get("date"),p.get("modified"),p.get("link"),"keys",list(p.keys()))
    print("TITLE",p.get("title"))
    urls=sorted(set(re.findall(r'https?:\\?/\\?/[^"\s<>]+',raw)))
    for u in urls:
        u=u.replace("\\/","/")
        if "wp-content/uploads" in u or "app.powerbi" in u: print("URL",u)
    # print any text-ish fields
    for k in ("acf","meta","excerpt","content"):
        if k in p: print("FIELD",k,json.dumps(p[k])[:3000])
    att=p.get("_links",{}).get("wp:attachment",[])
    for a in att:
        r=s.get(a["href"]+"&per_page=100",timeout=60)
        try:
            for m in r.json(): print("ATT",m.get("date"),m.get("source_url"),m.get("media_details",{}).get("filesize"))
        except Exception as e: print("ATTERR",e)
