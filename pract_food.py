import noms
import yaml

with open("config.yaml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)

client = noms.Client(cfg["noms_api_key"])

search_results = client.search_query("Raw Broccoli")
print(search_results)