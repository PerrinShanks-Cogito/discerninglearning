import requests, re, json
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (landmark-numbers)"})
u="https://data.england.nhs.uk/providers/guy-s-and-st-thomas-nhs-foundation-trust"
r=s.get(u,timeout=60); print("STATUS",r.status_code,r.headers.get("content-type"),len(r.text))
t=r.text
print("TEXT",re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",re.sub(r"(?s)<(script|style).*?</\1>","",t)))[:6000])
for m in sorted(set(re.findall(r'(?:href|src|action)="([^"]+)"',t))): print("LINK",m)
for m in sorted(set(re.findall(r'["\'](/api/[^"\']+|https?://[^"\']*api[^"\']*)["\']',t))): print("API",m)
for sc in re.findall(r'(?s)<script[^>]*>(.*?)</script>',t):
    if len(sc)>50: print("SCRIPT",sc[:1500].replace("\n"," "))
for p in ["/api/3/action/package_search?q=performance&rows=5","/api/3/action/status_show","/providers.json","/api/providers"]:
    try:
        rr=s.get("https://data.england.nhs.uk"+p,timeout=60); print("TRY",p,rr.status_code,rr.headers.get("content-type"),rr.text[:600].replace("\n"," "))
    except Exception as e: print("TRYERR",p,e)
