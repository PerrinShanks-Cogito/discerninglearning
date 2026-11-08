import requests, re, html
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
r=s.get("https://www.gov.uk/government/publications/spending-review-2025-document/spending-review-2025-html",timeout=90)
raw=r.text.encode().decode("unicode_escape",errors="ignore") if "\\u003c" in r.text else r.text
t=html.unescape(re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",raw)))
idx=[m.start() for m in re.finditer(r"Table 5\.14: Ministry of Defence",t)]
for i in idx: print("OCC",t[i:i+900]); print()
# 1794159049
