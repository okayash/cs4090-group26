# ...

import requests

url = "http://localhost:8000/api/users/"

user = {
  "username": "ashley",
  "first_name": "Ashley",
  "last_name": "Fong",
  "email": "akfkgx@umsystem.edu",
  "age": 21,
  "home_city": "Liberty"
}
r = requests.post(url, json=user)
print(r.status_code, r.json())