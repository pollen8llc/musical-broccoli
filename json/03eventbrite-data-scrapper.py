import requests
import json

all_events = []


def handle_data(events):
	for event in events:
		ev = {}
		ev["Event Name"] = event["name"]
		ev["Start Time"] = f"{event['start_date']} {event['start_time']}"
		ev["Address"] = f"{event['primary_venue']['address']['address_1']}, {event['primary_venue']['address']['city']}, {event['primary_venue']['address']['region']}, {event['primary_venue']['address']['country']}"
		#ev["Guest Count"] = 
		ev["Host"] = event["primary_organizer"]["name"]
		ev["Url"] = event["url"]

		all_events.append(ev)

url = "https://www.eventbrite.com/api/v3/destination/search/"
params = {
			"": "",
			"": ""
		}

cookies = {"csrftoken": "e194b5b051754f5f8fd49fc980e6b6eb"}
h = {"referer": "https://www.eventbrite.com/d/ny--new-york/events/",
			"X-CSRFToken": "e194b5b051754f5f8fd49fc980e6b6eb"
			}

headers = {
	"Accept": "*/*",
	"Accept-Encoding": "gzip, deflate, br, zstd",
	"Accept-Language": "en-US,en;q=0.5",
	"Cache-Control": "no-cache",
	"Connection":"keep-alive",
	"Content-Length":"512",
	"Content-Type":"application/json",
	"Cookie": "csrftoken=e194b5b051754f5f8fd49fc980e6b6eb; django_timezone=America/Chicago; _dd_s=rum=0&expire=1743907822892;",
	"Host": "www.eventbrite.com",
	"Origin": "https://www.eventbrite.com",
	"Pragma": "no-cache",
	"Prefer": "safe",
	"Priority": "u=4",
	"Referer": "https://www.eventbrite.com/d/ny--new-york/events/",
	"Sec-Fetch-Dest": "empty",
	"Sec-Fetch-Mode": "cors",
	"Sec-Fetch-Site": "same-origin",
	"TE": "trailers",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0",
	"X-CSRFToken": "e194b5b051754f5f8fd49fc980e6b6eb",
	"X-Requested-With": "XMLHttpRequest"
}

body = {
	"browse_surface": "browse",
	"event_search": {
		"dates": [
			"current_future"
		],
		"page_size": 50,
		"point_radius": {
			"latitude": 40.7151,
			"longitude": -73.984,
			"radius": "5mi"
		},
		"related_events": {
			"event_ids": [],
			"exclude_event_ids": True
		}
	},
	"expand.destination_event": [
		"primary_venue",
		"image",
		"ticket_availability",
		"saves",
		"event_sales_status",
		"primary_organizer",
		"public_collections"
	]
}

r = requests.request("POST", url, headers=headers, cookies=cookies, json=body)
res_json = r.json()

handle_data(res_json["events"]["results"])

# url = "https://www.eventbrite.com/api/v3/destination/events/"
# params = {
# 		"event_ids": "New York City Hiring Event",
# 		"expand": "event_sales_status,image,primary_venue,saves,ticket_availability,primary_organizer,public_collections",
# 		"page_size": 50,
# 		"include_parent_events": "true"
# 		}

# cookies = {"csrftoken": "e194b5b051754f5f8fd49fc980e6b6eb"}
# headers = {"referer": "https://www.eventbrite.com/d/ny--new-york/events/",
# 			"X-CSRFToken": "e194b5b051754f5f8fd49fc980e6b6eb"
# 			}

# r = requests.request("GET", url, headers=headers, cookies=cookies, params=params)
# res_json = r.json()
#print(res_json)


with open('EventBrite-events.json', 'w', encoding='utf-8') as f:
    json.dump(all_events, f, ensure_ascii=False, indent=4)