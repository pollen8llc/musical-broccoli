import requests
import json
import csv
import datetime

all_events_list = []

def deal_with_data():
    for entry in res_json["entries"]:
        event_list = {}
        event_list["Event Name"] = entry["event"]["name"]
        event_list["Start Time"] = entry["event"]["start_at"]
        event_list["Url"] = "https://lu.ma/" + entry["event"]["url"]
        try:
            event_list["Address"] = entry["event"]["geo_address_info"]["full_address"]
        except:
            event_list["Address"] = None

        event_list["Guest Count"] = entry["guest_count"]

        # Flatten host names into a comma-separated string
        hosts = [host["name"] for host in entry["hosts"]]
        try:
            event_list["Hosts"] = ", ".join(hosts)
        except TypeError:
            pass
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
csv_file = "csv_files/luma-events-" + datetime.datetime.now().strftime('%m-%d-%y')+ ".csv"
fieldnames = ["Event Name", "Start Time", "Address", "Guest Count", "Hosts","Url"]

with open(csv_file, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_events_list)