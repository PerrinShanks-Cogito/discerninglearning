import requests
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0 (Discerning Learning landmark numbers)"})
r=s.get("https://www.nomisweb.co.uk/api/v01/dataset/NM_30_1.data.csv?geography=K02000001,E92000001,W92000004,S92000003,N92000002&date=latest&sex=7,8&item=2&pay=7&measures=20100&select=date_name,geography_name,sex_name,pay_name,obs_value,obs_status_name",timeout=120)
print(r.text)
r=s.get("https://www.nomisweb.co.uk/api/v01/dataset/NM_30_1.data.csv?geography=K02000001&date=latest&sex=8&item=2&pay=7&measures=20100,20701&select=date_name,measures_name,obs_value",timeout=120)
print(r.text)
# 1794174960
# 1794175153
