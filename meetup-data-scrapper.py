import requests
import time
import json


def deal_with_data():
    for event in res_json["data"]["result"]["edges"]:
        print(event["node"]["title"])
        all_events.append(event)


# Paginated URL
url = "	https://www.meetup.com/gql2"
params = {

}

h = {"referer": "https://www.meetup.com/find/?location=us--ny--New%20York%20City&source=EVENTS",
     "Cookie": "MEETUP_BROWSER_ID=id=adf0d936-ae6c-404e-927d-811d242d2f1c; MEETUP_TRACK=id=9593bf77-999f-4ae9-9122-040411e4a015; SIFT_SESSION_ID=3c494806-b1d3-4452-82e9-c79fcc39cf42; LOGGED_OUT_HOMEPAGE_SEGMENTATION=login_spotlight; __stripe_mid=5d8ba31d-7a23-40eb-a8d9-a4bb498769165af78f; __stripe_sid=240c5225-f58f-45f5-abe5-bfd21f77d44304ab67; MEETUP_MEMBER_LOCATION=city=New+York+City&country=us&localized_country_name=us&state=NY&name_string=New+York+City%252C+NY%252C+USA&zip=10044&lat=40.7599983215332&lon=-73.94999694824219&borough=&neighborhood=&timeZone=America%252FChicago; FIND_REVAMP_SEGMENTATION_v3=control; USER_CHANGED_DISTANCE_FILTER=false; __Host-NEXT_MEETUP_CSRF=b54edc86-feb4-45f5-81a4-14c6f977f22b",
     "content-type": "application/json",
     "Origin": "https://www.meetup.com",
     "Accept": "*/*"
     }

body = {
    "extensions": {
        "persistedQuery": {
            "sha256Hash": "4b0e4ad488864d476bd860c73ec1ac8fc5cd951b89c5cf6aeecf2cbb822c992d",
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

r = requests.request("POST", url, params=params, json=body)
res_json = r.json()

deal_with_data()

while True:
    if res_json["data"]["result"]["pageInfo"]["hasNextPage"]:
        time.sleep(5)
        body["variables"]["after"] = res_json["data"]["result"]["pageInfo"]["endCursor"]
        r = requests.request("POST", url, params=params, json=body)
        res_json = r.json()

        deal_with_data()
    else:
        break

with open('meetup_data.json', 'w', encoding='utf-8') as f:
    json.dump(all_events, f, ensure_ascii=False, indent=4)