import requests
import json
import datetime
import csv

url = "https://www.supermomos.com/api/getPastSocialsV2"

all_events_list = []

# Paginated URL
params = {
    "city": "New York",
    "exclusiveStart": ""
}

while True:
    r = requests.get(url, params=params)
    res_json = r.json()

    events_list = res_json["data"]["New York"]

    if not events_list:
        break  # No more events

    all_events_list.extend(events_list)

    # Convert ISO 8601 string to datetime object
    last_event_time = datetime.datetime.fromisoformat(events_list[-1]["eventTimestamp"].replace("Z", "+00:00"))

    if last_event_time < datetime.datetime(2025, 4, 16, tzinfo=datetime.timezone.utc):
        break

    # Update pagination key
    last_key = res_json.get("meta", {}).get("lastEvaluatedKey")
    if not last_key:
        break  # No more pages

    params["exclusiveStart"] = last_key

# Print all fetched events
print(f"Total events fetched: {len(all_events_list)}")
for event in all_events_list:
    print(event)

# Choose fields to include in CSV
fieldnames = [
    "title",
    "eventTimestamp",
    "location",
    "attendeeCount",
    "tags",
    "description"
]

# Save to CSV file
with open("supermomos_events.csv", mode="w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for event in all_events_list:
        # Write only selected fields, handling missing keys
        writer.writerow({key: event.get(key, "") for key in fieldnames})

print("✅ Events exported to supermomos_events.csv")

