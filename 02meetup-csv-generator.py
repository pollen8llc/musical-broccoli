import requests
import time
import csv
import datetime

def deal_with_data():
    for event in res_json["data"]["result"]["edges"]:
        event_list = {}
        event_list["Event Name"] = event["node"]["title"]
        event_list["Start Time"] = event["node"]["dateTime"]

        try:
            event_list["Address"] = event["node"]["venue"]["address"]
        except:
            event_list["Address"] = None

        event_list["Guest Count"] = event["node"]["rsvps"]["totalCount"]

        event_list["Hosts"] = []
        for rsvp in event["node"]["rsvps"]["edges"]:
            if rsvp["node"]["isHost"]:
               event_list["Hosts"].append(rsvp["node"]["user"]["name"])
        event_list["Description"] = event["node"]["description"]
        event_list["Url"] = event["node"]["eventUrl"]
        print(event["node"]["title"])
        all_events.append(event_list)

# Paginated URL
url = "https://www.meetup.com/gql2"
params = {}

h = {
    "referer": "https://www.meetup.com/find/?location=us--ny--New%20York%20City&source=EVENTS",
    "Cookie": "your_cookie_here",  # Recuerda reemplazar esto si es necesario.
    "content-type": "application/json",
    "Origin": "https://www.meetup.com",
    "Accept": "*/*"
}

body = {
    "extensions": {
        "persistedQuery": {
            "sha256Hash": "23a3bb8cf7dd8f0e806c265be70fd604eae93ba9cced577c5f51c94889d3901f",
            "version": "1"
        }
    },
    "operationName": "recommendedEventsWithSeries",
    "variables": {
        "after": "",
        "dataConfiguration": "{\"isSimplifiedSearchEnabled\": true, \"include_events_from_user_chapters\": true}",
        "doConsolidateEvents": "true",
        "doPromotePaypalEvents": "false",
        "first": "20",
        "indexAlias": "\"{\\\"filterOutWrongLanguage\\\": \\\"true\\\",\\\"modelVersion\\\": \\\"split_offline_online\\\"}\"",
        "lat": "40.7599983215332",
        "lon": "-73.94999694824219",
        "numberOfEventsForSeries": "5",
        "seriesStartDate": "2025-04-05",
        "sortField": "RELEVANCE",
        "startDateRange": "2025-04-05T18:17:56-04:00[US/Eastern]"
    }
}

all_events = []

r = requests.request("POST", url, params=params, json=body, headers=h)
res_json = r.json()
deal_with_data()

while True:
    if res_json["data"]["result"]["pageInfo"]["hasNextPage"]:
        time.sleep(5)
        body["variables"]["after"] = res_json["data"]["result"]["pageInfo"]["endCursor"]
        r = requests.request("POST", url, params=params, json=body, headers=h)
        res_json = r.json()
        deal_with_data()
    else:
        break

# Save as CSV
csv_filename = "csv_files/" + datetime.datetime.now().strftime('%m-%d-%y') + "-meetup-events.csv"
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ["Event Name", "Start Time", "Address", "Guest Count", "Hosts", "Url","Description"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for event in all_events:
        event["Hosts"] = ", ".join(event["Hosts"])  # Convert list to comma-separated string
        writer.writerow(event)

print(f"CSV file generated: {csv_filename}")