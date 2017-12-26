import speedtest
import requests

s = speedtest.Speedtest()

config = s.get_config()

r = requests.post('http://localhost:8000', data=config)



# print(s.get_best_server())
# print(s.download())
# print(s.upload())
#
# print(s.results.dict())
