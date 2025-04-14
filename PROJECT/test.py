import requests
import json

res = requests.get("http://127.0.0.1:5000/api/history")
data = res.json()
print(json.dumps(data, ensure_ascii=False, indent=2))
