import requests, re, html, json
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (landmark-numbers)"})
for code in ["ae_4_hour","cancer_62_day"]:
    r=s.post("https://data.england.nhs.uk/api/export/json",data={"metricCode":code,"providerCode":"RJ1","includeNational":"true"},timeout=60)
    print("JSON",code,r.status_code,r.headers.get("content-type"),r.text[:2500])
t=s.get("https://data.england.nhs.uk/providers/guy-s-and-st-thomas-nhs-foundation-trust",timeout=60).text
txt=html.unescape(re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",re.sub(r"(?s)<(script|style).*?</\1>","",t))))
for m in re.finditer(r"(?:Elective|Cancer|Diagnostics|A&E|Accident)[^.]{0,80}?This metric|The standard reflects|Current Performance ([\d.]+%) Rank: (\d+) of (\d+) National Average ([\d.]+%)|latest available at (\w+ \d{4})",txt):
    print("M",m.group(0)[:160])
i=txt.find("Diagnostics Diagnostics"); print("DIAG",txt[i:i+700]); j=txt.find("Accident and Emergency A&E"); print("AE",txt[j-100:j+1500])
