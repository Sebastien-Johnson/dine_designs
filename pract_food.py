import yaml
import requests
import json

def get_food():
    with open("config.yaml", "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
        food = "Ground beef"
        key = str(cfg["usda_api_key"])
       
        headers={"x-api-key":key}
        url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={food}"

        response = requests.get(url, headers=headers)
        json_text = json.dumps(response.json(), indent=2)
        print(json_text)

get_food()