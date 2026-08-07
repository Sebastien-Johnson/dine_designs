import yaml
import requests
import json

class food_item():
    def __init__(self, name, protiens, carbs, fats, fiber, base_calories, base_serving, unit):
        self.name = name
        self.protiens = protiens
        self.carbs = carbs
        self.fats = fats
        self.fiber = fiber
        self.calories = base_calories
        self.base_serving = base_serving
        self.unit = unit

    macros_codes = {
        "protein_num" : 203,
        "protien_id" : 1003,
        "carbs_num" : 205,
        "carbs_id" : 1005,
        "fat_num" : 204,
        "fat_id" : 1004,
        "fiber_num" : 291,
        "fiber_id" : 1079,
    }

    macro_names = {
        "proteins" : "Protein",
        "carbs" : "Carbohydrate, by difference",
        "calories" : "Energy",
        "fats" : "Total lipid (fat)",
        "fiber" : "Fiber, total dietary"
    }
    

    def get_info(self):
        serving_info = self.scale_macros()
        serving_scale = serving_info[0]
        print(f"scale: {serving_scale}")
        desired_serving = serving_info[1]
        print(f"name: {self.name}")
        print(f"proteins: {round((self.protiens*serving_scale), 1)} g")
        print(f"carbs: {round((self.carbs*serving_scale), 1)} g")
        print(f"fats: {round((self.fats*serving_scale), 1)} g")
        print(f"fiber: {round((self.fiber*serving_scale), 1)} g")
        print(f"calories: {round((self.calories*serving_scale), 1)} cal")
        print(f"serving size: {desired_serving} {self.unit}")

    def get_desired_serving(self):
        #check if num or alpha
        print(f"Enter amount ({self.unit})")
        desired_serving = input()
        return desired_serving
    
    def scale_macros(self):
        desired_serving = float(self.get_desired_serving())
        serving_scale = round((desired_serving/self.base_serving), 2)
        return (serving_scale, desired_serving)

def get_api_foods():
    with open("config.yaml", "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
        key = str(cfg["usda_api_key"])

        print("Enter next ingredient")
        food_req = input()
        
    
        headers={"x-api-key":key}
        url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={food_req}"

        response = requests.get(url, headers=headers)
        food = response.json()["foods"]
        #iterate through all food options/"descriptions" and choose
        
        new_food = create_food_item(food[0])
        new_food.get_info()


def create_food_item(food):
    nutrients = food["foodNutrients"]
    macros = [
        ["protien", 1.0],
        ["carb", 1.0],
        ["fat", 1.0],
        ["fiber", 1.0],
        ["energy", 1.0],
    ]
    print(macros[0][0])
    for nutrient in nutrients:
        for macro in macros:
            if macro[0].lower() in nutrient["nutrientName"].lower():
                macro[1] = nutrient["value"]

    new_food = food_item(
                        food["description"], 
                        float(macros[0][1]), 
                        float(macros[1][1]), 
                        float(macros[2][1]), 
                        float(macros[3][1]), 
                        float(macros[4][1]), 
                        float(food["servingSize"]),
                        food["servingSizeUnit"]
                    )

    return new_food

get_api_foods()