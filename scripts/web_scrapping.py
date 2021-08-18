import urllib3
import json
import pandas as pd

target_url = "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/"

with open("filename.txt", "r") as f:
  datasets = f.read().splitlines()

print(len(datasets))

df = pd.DataFrame(columns=['dataset', 'bounds', 'boundsConforming', 'points'])
http = urllib3.PoolManager()
for d in datasets:
  r = http.request('GET', target_url + d + "ept.json")
  if r.status == 200:
    j = json.loads(r.data)
    df = df.append({'dataset': d, 'bounds': j['bounds'], 'boundsConforming': j['boundsConforming'], 'points': j['points']}, ignore_index=True)

# print(df.head())
df.to_csv(r'../data/metadata.csv', index=False, header=True)
