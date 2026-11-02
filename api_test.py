import os
import requests

API_KEY = os.environ.get("ANIMALS_API_KEY")

url = "https://api.api-ninjas.com/v1/animals"
headers = {"X-Api-Key": API_KEY}
params = {"name": "fox"}

response = requests.get(url, headers=headers, params=params, timeout=30)
print("Status code:", response.status_code)
print(response.json())

if response.status_code == 200:
    animals_data = response.json()

    print(f"Animals returned: {len(animals_data)}")

    for animal in animals_data:
        print(animal["name"])
else:
    print(response.json())