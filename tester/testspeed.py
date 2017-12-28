import requests
import speedtest

s = speedtest.Speedtest()
config = s.get_config()

# client
client = s.config['client']

r = requests.get("http://localhost:8000/api/clients?ip={0}&isp={1}".format(client["ip"], client["isp"]))
if r.ok and len(r.json()) == 1:
    print("Found client {0} (id:{1}) ".format(r.json()[0]["isp"], r.json()[0]["id"]))
    client_id = r.json()[0]["id"]
else:
    print("Creating client {0} (ip:{1})".format(client["isp"], client["ip"]))
    r = requests.post('http://localhost:8000/api/clients', json=s.config['client'])
    if r.ok:
        print("Created client {0} (id:{1}) ".format(r.json()["isp"], r.json()["id"]))
        client_id = r.json()["id"]
    else:
        print("Woopsie.")

# server
s.get_best_server()

r = requests.get('http://localhost:8000/api/servers?url={0}'.format(s.best["url"]))
if r.ok and len(r.json()) == 1:
    print("Found server {0} (id:{1}) ".format(r.json()[0]["url"], r.json()[0]["id"]))
    server_id = r.json()[0]["id"]
else:
    print("Creating server {0} (name:{1})".format(s.best["url"], s.best["name"]))
    r = requests.post('http://localhost:8000/api/servers', json=s.best)
    if r.ok:
        print("Created server {0} (id:{1}) ".format(r.json()["url"], r.json()["id"]))
        server_id = r.json()["id"]
    else:
        print("Woopsie.")

# test the speed of the link
print(s.download())
print(s.upload())

# prepare the result...
result = s.results.dict()
result["client"] = client_id
result["server"] = server_id

# ...and send it to the monitor
r = requests.post('http://localhost:8000/api/results', json=result)
if r.ok:
    print("Added result [up:{0}, down:{1}] ".format(result["upload"], result["download"]))
else:
    print("Woopsie.")
