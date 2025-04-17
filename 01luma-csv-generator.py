import requests
import json
import csv

all_events_list = []

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

        # Flatten host names into a comma-separated string
        hosts = [host["name"] for host in entry["hosts"]]
        event_list["hosts"] = ", ".join(hosts)

        all_events_list.append(event_list)


# Paginated URL
url = "https://api.lu.ma/discover/get-paginated-events"
params = {
    "discover_place_api_id": "discplace-Izx1rQVSh8njYpP",
    "pagination_cursor": ""
}

r = requests.get(url, params=params)
res_json = r.json()
deal_with_data()

while res_json.get("has_more"):
    params["pagination_cursor"] = res_json["next_cursor"]
    r = requests.get(url, params=params)
    res_json = r.json()
    deal_with_data()

# Write to CSV
csv_file = "csv_files/luma-events.csv"
fieldnames = ["name", "start_time", "timezone", "address", "guest_count", "hosts"]

with open(csv_file, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_events_list)