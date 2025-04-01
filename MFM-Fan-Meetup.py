import requests
url = "https://app.getriver.io/beta/events/mfm-fan-meetup-nyc-8i6"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
print(response.text)  # Check if the event details appear