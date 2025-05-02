import requests
import json


def deal_with_data():
    for entry in res_json["entries"]:
        event_list = {}
        event_list["name"] = entry["event"]["name"]
        event_list["start_time"] = entry["event"]["start_at"]
        event_list["timezone"] = entry["event"]["timezone"]
        try:
            event_list["address"] = entry["event"]["geo_address_info"]["full_address"]
        except:
            event_list["address"] = None

        event_list["guest_count"] = entry["guest_count"]

        # event_list["host"] = entry["hosts"]
        event_list["hosts"] = []
        for host in entry["hosts"]:
            event_list["hosts"].append(host["name"])

        all_events_list.append(event_list)


# Main URL
# url = "https://lu.ma/nyc"

all_events_list = []

# Paginated URL
url = "https://api.lu.ma/discover/get-paginated-events"
params = {
    "discover_place_api_id": "discplace-Izx1rQVSh8njYpP",
    "pagination_cursor": ""
}

r = requests.request("GET", url, params=params)
res_json = r.json()

# for entry in json["entries"]:
# 	print(entry["event"]["name"])
deal_with_data()

while True:

    if res_json["has_more"]:
        params = {
            "discover_place_api_id": "discplace-Izx1rQVSh8njYpP",
            "pagination_cursor": res_json["next_cursor"]}
        r = requests.request("GET", url, params=params)
        res_json = r.json()
        deal_with_data()
    else:
        break

# final_json = json.dumps(all_events_list)
# print(final_json)

with open('luma-data.json', 'w', encoding='utf-8') as f:
    json.dump(all_events_list, f, ensure_ascii=False, indent=4)