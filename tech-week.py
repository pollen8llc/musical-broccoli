import requests
import csv
import datetime  # Import datetime module

url = "https://api.tech-week.com/list_events/?city=NYC&_=1746669652613"

r = requests.get(url)
events = r.json()

all_events_list = []

for event in events:
    data = {
        "Name": event["event_name"],
        "Address": f'{event["neighborhood"]}, {event["city"]}',
        "Date": event["start_time"],
        "Hosts": ', '.join(event["hosts"]) if isinstance(event["hosts"], list) else event["hosts"],
        "Url": event["invite_url"]
    }
    all_events_list.append(data)

# Save as CSV with current date in filename
csv_file = "csv_files/" + datetime.datetime.now().strftime('%m-%d-%y') + "-tech-week-events.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Name", "Address", "Date", "Hosts", "Url"])
    writer.writeheader()
    writer.writerows(all_events_list)