import requests
from bs4 import BeautifulSoup

# URL of the page to scrape
url = "https://foundersfundersandfriends.com/members"

# Headers to mimic a real browser visit
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Send a GET request
response = requests.get(url, headers=headers)

# Check if request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # Example: Find member sections (adjust selectors as needed)
    members = soup.find_all("div", class_="member-card")

    for member in members:
        name = member.find("h2").text.strip() if member.find("h2") else "N/A"
        title = member.find("p", class_="title").text.strip() if member.find("p", class_="title") else "N/A"

        print(f"Name: {name}, Title: {title}")
else:
    print(f"Failed to retrieve page. Status code: {response.status_code}")
