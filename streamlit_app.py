import requests
import json

item_id = 17584
url = f"https://api.dofusdu.de/dofus3/v1/fr/items/equipments/{item_id}"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=4, ensure_ascii=False))
else:
    print(f"Erreur : {response.status_code}")

