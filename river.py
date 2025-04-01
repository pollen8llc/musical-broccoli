from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (optional)
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Open the website
url = "https://app.getriver.io/coffee-club"
driver.get(url)

# Wait for the page to load
time.sleep(5)  # Allow time for JavaScript to load content

# Debug: Print page title
print("Page title:", driver.title)

# Debug: Print part of the page source
print("Page source (truncated):", driver.page_source[:1000])  # Print first 1000 chars

# Wait for events to load
try:
    events = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "event-card"))  # Adjust class name
    )

    # Extract event titles
    print("\nUpcoming Events:")
    for event in events:
        title = event.find_element(By.TAG_NAME, "h2").text.strip()  # Adjust tag if needed
        print("-", title)

except Exception as e:
    print("Error:", e)

# Close browser
driver.quit()