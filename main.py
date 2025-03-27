import requests

def deal_with_data():
	for entry in json["entries"]:
		print(entry["event"]["name"])

# Main URL
# url = "https://lu.ma/nyc"

# Paginated URL
url = "https://api.lu.ma/discover/get-paginated-events"
params = {
			"discover_place_api_id": "discplace-Izx1rQVSh8njYpP",
			"pagination_cursor": ""
		}

r = requests.request("GET", url, params=params)
json = r.json()

# for entry in json["entries"]:
# 	print(entry["event"]["name"])
deal_with_data()

while True:

	if json["has_more"]:
		params = {
			"discover_place_api_id": "discplace-Izx1rQVSh8njYpP",
			"pagination_cursor": json["next_cursor"]}
		r = requests.request("GET", url, params=params)
		json = r.json()
		deal_with_data()
	else:
		break
