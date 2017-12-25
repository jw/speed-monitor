import speedtest

s = speedtest.Speedtest()

print(s.get_config())
print(s.get_best_server())
print(s.download())
print(s.upload())

print(s.results.dict())
