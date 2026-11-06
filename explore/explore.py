import requests, re, json
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (landmark-numbers)"})
for pid in [294161,275980]:
    raw=json.dumps(s.get(f"https://www.england.nhs.uk/wp-json/wp/v2/documents/{pid}",timeout=60).json())
    for m in re.finditer(r"app\.powerbi\.com",raw):
        print(pid,"CONTEXT",raw[max(0,m.start()-700):m.start()+200].replace("\\n"," "))
        print()
