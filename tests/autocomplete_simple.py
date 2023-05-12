import requests

url = "https://maps.googleapis.com/maps/api/place/autocomplete/json?input=california&types=postal_town&location=37.76999%2C-122.44696&radius=50000000&strictbounds=true&key=AIzaSyAjE6UiHJdgkgDLJ5zDM2upMuX81b15WZI"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)