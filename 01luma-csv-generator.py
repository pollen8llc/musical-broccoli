import requests
import json
import csv
import datetime
import os

all_events_list = []

def deal_with_data():
    for entry in res_json["entries"]:
        event_list = {
            "Event Name": entry["event"]["name"],
            "Start Time": entry["event"]["start_at"],
            "Url": "https://lu.ma/" + entry["event"]["url"],
            "Guest Count": entry["guest_count"]
        }

        try:
            event_list["Address"] = entry["event"]["geo_address_info"]["full_address"]
        except:
            event_list["Address"] = None

        try:
            hosts = [host["name"] for host in entry["hosts"]]
            event_list["Hosts"] = ", ".join(hosts)
        except TypeError:
            event_list["Hosts"] = None

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

# Create directory if not exists
os.makedirs("csv_files", exist_ok=True)

# Save to CSV file with BOM for Excel
csv_file = "csv_files/luma-events-" + datetime.datetime.now().strftime('%m-%d-%y') + ".csv"
fieldnames = ["Event Name", "Start Time", "Address", "Guest Count", "Hosts", "Url"]

with open(csv_file, mode='w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_events_list)

print(f"Events exported successfully to {csv_file}")