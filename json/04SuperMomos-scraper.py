import requests
import json
import datetime
import csv
import os


all_events_list = []

# url = "https://www.supermomos.com/api/getPastSocialsV2"
url = " https://www.supermomos.com/api/getPublicSocialsV2"
params = {
    "city": "New York",
    "exclusiveStart": ""
}

def deal_with_data(events):
    
    for event in events:
        ev = {}
        print(event["title"])
        ev["Name"] = event["title"]
        ev["Start Time"] = event["eventTimestamp"]
        ev["Address"] = event["venueData"]["address"]
        ev["Capacity"] = event["maxCapacity"]
        ev["Hosts"] = []
        for host in event["hosts"]:
            fullname = host["firstName"] + " " + host["lastName"]
            ev["Hosts"].append(fullname)
        ev["Url"] = "https://www.supermomos.com/socials/" + event["slug"]

        all_events_list.append(ev)


while True:

    r = requests.get(url, params=params)

    if r.status_code != 200:
        print(f"Request failed with status code {r.status_code}")
        break

    res_json = r.json()

    if "New York" not in res_json:
        print("Missing expected keys in response.")
        print(res_json)
        break

    print(res_json["New York"])
    events_list = res_json["New York"]

    # if not events_list:
    #     break

    # try:
    #     last_event_time = datetime.datetime.fromisoformat(
    #         events_list[-1]["eventTimestamp"].replace("Z", "+00:00")
    #     )
    # except Exception as e:
    #     print(f"Error parsing date: {e}")
    #     break

    # if last_event_time > datetime.datetime(2025, 4, 16, tzinfo=datetime.timezone.utc):
    #     break

    deal_with_data(events_list)

    # last_key = res_json.get("meta", {}).get("lastEvaluatedKey")
    # if not last_key:
    #     break

    # params["exclusiveStart"] = last_key
    break

print(f"Total events fetched: {len(all_events_list)}")

# Save to CSV with timestamp
os.makedirs("csv_files", exist_ok=True)
csv_filename = 'csv_files/supermomos-events-' + datetime.datetime.now().strftime('%m-%d-%y') + '.csv'


with open(csv_filename, 'w', encoding='utf-8') as f:
    json.dump(all_events_list, f, ensure_ascii=False, indent=4)