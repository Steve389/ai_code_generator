import requests

response = requests.post("http://localhost:5000/items", json={"name": "new_item"})