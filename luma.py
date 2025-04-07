import requests
import json
import csv

# List to hold all the event data
all_events_list = []

# Function to process each page of data
def deal_with_data():
    for entry in res_json["entries"]:
        event_list = {
            "name": entry["event"]["name"],
            "start_time": entry["event"]["start_at"],
            "timezone": entry["event"]["timezone"],
            "guest_count": entry["guest_count"],
        }

        try:
            event_list["address"] = entry["event"]["geo_address_info"]["full_address"]
        except:
            event_list["address"] = None

        event_list["hosts"] = [host["name"] for host in entry["hosts"]]

        all_events_list.append(event_list)

# Initial request URL and parameters
url = "https://api.lu.ma/discover/get-paginated-events"
params = {
    "discover_place_api_id": "discplace-Izx1rQVSh8njYpP",
    "pagination_cursor": ""
}

# First API request
r = requests.get(url, params=params)
res_json = r.json()
deal_with_data()

# Pagination loop
while res_json.get("has_more"):
    params["pagination_cursor"] = res_json["next_cursor"]
    r = requests.get(url, params=params)
    res_json = r.json()
    deal_with_data()

# Write to JSON file
json_file = 'luma-updated-data.json'
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(all_events_list, f, ensure_ascii=False, indent=4)

# Write to CSV file
csv_file = 'luma-updated-data.csv'
if all_events_list:
    # Flatten hosts list to a comma-separated string for CSV
    for event in all_events_list:
        # Only join non-None values in the hosts list
        event["hosts"] = ", ".join([host for host in event["hosts"] if host is not None])

    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=all_events_list[0].keys())
        writer.writeheader()
        writer.writerows(all_events_list)