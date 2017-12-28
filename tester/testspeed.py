import speedtest
import requests

s = speedtest.Speedtest()

config = s.get_config()

r = requests.post('http://localhost:8000/api/clients', json=s.config['client'])
print(r.ok)
print(r.json())
print("client {0} ({1}) ".format(r.json()["isp"], r.json()["id"]))

s.get_best_server()

r = requests.post('http://localhost:8000/api/servers', json=s.best)
print(r.json())
print("server {0} in {1} ({2})".format(r.json()["name"], r.json()["country"], r.json()["id"]))

# print(s.download())
# print(s.upload())
#
# print(s.results.dict())
