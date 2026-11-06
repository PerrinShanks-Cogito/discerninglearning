import requests, re, html
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (landmark-numbers)"})
u="https://data.england.nhs.uk/providers/guy-s-and-st-thomas-nhs-foundation-trust"
t=s.get(u,timeout=60).text
txt=html.unescape(re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",re.sub(r"(?s)<(script|style).*?</\1>","",t))))
i=txt.find("Elective proportion waiting within 18 weeks This metric")
print("FULL",txt[i:i+20000])
for m in re.finditer(r'<form[^>]*action="/api/export/(json|csv)"[^>]*>(.*?)</form>',t,re.S): print("FORM",m.group(0)[:1500])
for p in ["/api/export/json","/api/export/json?provider=RJ1","/providers"]:
    r=s.get("https://data.england.nhs.uk"+p,timeout=60); print("TRY",p,r.status_code,r.headers.get("content-type"),html.unescape(re.sub(r"<[^>]+>"," ",r.text))[:1500].replace("\n"," "))
r=s.get("https://data.england.nhs.uk/providers",timeout=60)
links=sorted(set(re.findall(r'href="(/providers/[^"#?]+)"',r.text))); print("NPROV",len(links)); print(links[:400])
