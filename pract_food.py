import yaml
import requests
import json
from requests.auth import HTTPBasicAuth

def get_food():
    with open("config.yaml", "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
        food = "Cheese"
        key = str(cfg["usda_api_key"])
       
        headers={"x-api-key":key, "query":food}
        url = f"https://api.nal.usda.gov/fdc/v1/foods/search?"

        response = requests.get(url, headers=headers)
        print(json.dumps(response.json(), indent=2))
        
get_food()