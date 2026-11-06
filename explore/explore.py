import requests, re, json
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (landmark-numbers)"})
B="https://www.england.nhs.uk/wp-json/wp/v2/"
r=s.get(B+"search?per_page=20&search="+requests.utils.quote("national cost collection data publication"),timeout=60)
print("SEARCH",r.status_code)
for it in r.json(): print("HIT",it.get("title"),it.get("url"),it.get("subtype"),[l.get("href") for l in it.get("_links",{}).get("self",[])])
for it in r.json():
    if "2024-25" in it.get("url","") or "2023-24" in it.get("url",""):
        for l in it["_links"]["self"]:
            p=s.get(l["href"],timeout=60).json()
            html=p.get("content",{}).get("rendered","")
            print("\nPAGE",it["url"],p.get("date"),p.get("modified"))
            print("TEXT",re.sub(r"<[^>]+>"," ",html)[:2500])
            for h in sorted(set(re.findall(r'href="([^"]+)"',html))): print("PLINK",h)
for q in ["24-25","2425","2024-25","23-24","2324"]:
    r=s.get(B+"media?per_page=100&search="+q,timeout=60)
    for m in r.json():
        u=m.get("source_url","")
        if re.search(r"(ncc|cost|schedule|ncci|organisation)",u,re.I): print("MEDIA",q,m.get("date"),u)
