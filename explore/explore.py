import requests, re, html
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
r=s.get("https://www.gov.uk/government/publications/spending-review-2025-document/spending-review-2025-html",timeout=90)
t=html.unescape(re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",r.text)))
i=t.find("Table 5.14: Ministry of Defence"); print(t[i:i+1600])
# 1794159010
