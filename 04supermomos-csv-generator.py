import requests
import datetime
import csv
import os

all_events_list = []

url = "https://www.supermomos.com/api/getPublicSocialsV2"
params = {
    "city": "New York",
    "exclusiveStart": ""
}

def deal_with_data(events):
    for event in events:
        hosts = [host["firstName"] + " " + host["lastName"] for host in event.get("hosts", [])]
        ev = {
            "Name": event.get("title", ""),
            "Start Time": event.get("eventTimestamp", ""),
            "Address": event.get("venueData", {}).get("address", ""),
            "Capacity": event.get("maxCapacity", ""),
            "Hosts": ", ".join(hosts),
            "Url": f"https://www.supermomos.com/socials/{event.get('slug', '')}"
        }
        all_events_list.append(ev)

# Pagination loop
while True:
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Failed to fetch data: HTTP {response.status_code}")
        break

    data = response.json()

    if "New York" not in data or not data["New York"]:
        print("No more events or data not in expected format.")
        break

    events_list = data["New York"]
    deal_with_data(events_list)

    # Check if more pages exist
    last_key = data.get("meta", {}).get("lastEvaluatedKey")
    if not last_key:
        break
    params["exclusiveStart"] = last_key

print(f"Total events fetched: {len(all_events_list)}")

# Save to CSV
os.makedirs("csv_files", exist_ok=True)
csv_filename = f'csv_files/{datetime.datetime.now().strftime("%m-%d-%y")}-supermomos-events.csv'

with open(csv_filename, 'w', encoding='utf-8', newline='') as f:
    fieldnames = ["Name", "Start Time", "Address", "Capacity", "Hosts", "Url"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for event in all_events_list:
        writer.writerow(event)

print(f"Saved to {csv_filename}")