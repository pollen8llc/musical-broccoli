import requests
import csv

def fetch_events():
    url = "https://api.lu.ma/discover/get-paginated-events"
    params = {
        "discover_place_api_id": "discplace-Izx1rQVSh8njYpP",
        "pagination_cursor": ""
    }

    all_events = []

    while True:
        response = requests.get(url, params=params)
        json_data = response.json()

        for entry in json_data["entries"]:
            event_data = entry["event"]
            all_events.append(event_data)  # Store all event details

        if not json_data.get("has_more", False):
            break  # Stop if there are no more pages

        params["pagination_cursor"] = json_data["next_cursor"]

    return all_events

def save_to_csv(events, filename="events.csv"):
    if not events:
        print("No event data found.")
        return

    # Get all possible keys from event data
    keys = events[0].keys()

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()  # Write the header row
        writer.writerows(events)  # Write all event data

    print(f"CSV file '{filename}' has been saved successfully.")

# Fetch events and save them to CSV
events = fetch_events()
save_to_csv(events)