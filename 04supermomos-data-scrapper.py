import requests
import json
import datetime
import csv
import os

url = "https://www.supermomos.com/api/getPastSocialsV2"
params = {
    "city": "New York",
    "exclusiveStart": ""
}

all_events_list = []

while True:
    r = requests.get(url, params=params)

    if r.status_code != 200:
        print(f"Request failed with status code {r.status_code}")
        break

    res_json = r.json()

    if "data" not in res_json or "New York" not in res_json["data"]:
        print("Missing expected keys in response.")
        print(res_json)
        break

    events_list = res_json["data"]["New York"]

    if not events_list:
        break

    all_events_list.extend(events_list)

    try:
        last_event_time = datetime.datetime.fromisoformat(
            events_list[-1]["eventTimestamp"].replace("Z", "+00:00")
        )
    except Exception as e:
        print(f"Error parsing date: {e}")
        break

    if last_event_time < datetime.datetime(2025, 4, 16, tzinfo=datetime.timezone.utc):
        break

    last_key = res_json.get("meta", {}).get("lastEvaluatedKey")
    if not last_key:
        break

    params["exclusiveStart"] = last_key

print(f"Total events fetched: {len(all_events_list)}")

# Save to CSV with timestamp
os.makedirs("csv_files", exist_ok=True)
csv_filename = 'csv_files/supermomos-events-' + datetime.datetime.now().strftime('%m-%d-%y') + '.csv'

fieldnames = [
    "title",
    "eventTimestamp",
    "location",
    "attendeeCount",
    "tags",
    "description"
]

with open(csv_filename, mode="w", newline="", encoding="utf-8-sig") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for event in all_events_list:
        writer.writerow({key: event.get(key, "") for key in fieldnames})

print(f"Events exported to {csv_filename}")
