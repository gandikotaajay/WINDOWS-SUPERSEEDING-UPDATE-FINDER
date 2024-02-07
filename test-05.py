import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime

if len(sys.argv) != 2:
    print("Usage: python3 test-03.py <initial_url>")
    sys.exit(1)

# Get the initial URL from command-line argument
initial_url = sys.argv[1]

# Send a GET request to the initial URL
response = requests.get(initial_url)

# Parse the HTML content of the webpage
soup = BeautifulSoup(response.content, 'html.parser')

# Find all elements with class 'supLeftNavLink'
links = soup.find_all(class_='supLeftNavLink')

latest_date = None
latest_href = None

# Loop through each element to find the latest date
for link in links:
    date_str = link.text.split("—")[0].strip()  # Extract date string

    try:
        date_obj = datetime.strptime(date_str, "%B %d, %Y")  # Convert date string to datetime object
    except ValueError:
        continue  # Skip this element if it doesn't represent a valid date

    # Check if the current date is the latest
    if latest_date is None or date_obj > latest_date:
        latest_date = date_obj
        latest_href = link.get('href')

# Check if a valid date was found in the elements
if latest_date:
   # print("Latest Date:", latest_date.strftime("%B %d, %Y"))
   # print("Corresponding Href:", latest_href)

    # Extract the value after "help/"
    href_value = latest_href.split('/')[-1]

    # Construct the new URL
    new_url = f"https://support.microsoft.com/help/{href_value}"

   # print("New URL:", new_url)
else:
#    print(initial_url)
    new_url = initial_url

# Continue with the script using the URL
# Send a GET request to the URL with follow redirects enabled
response = requests.get(new_url, allow_redirects=True)

# Parse the HTML content of the redirected webpage
soup = BeautifulSoup(response.content, 'html.parser')

# Find all <a> tags (links) in the redirected webpage
links = soup.find_all('a')

specified_url = "https://www.catalog.update.microsoft.com/Search.aspx"

# Flag to track if any relevant links were found
found_relevant_link = False

for link in links:
    href = link.get('href')  # Get the value of the 'href' attribute
    if href and href.startswith(specified_url):
        print(href)
        found_relevant_link = True

# If no relevant link was found, print the KB search URL
if not found_relevant_link:
    specified_url_kb = f"{specified_url}?q=KB{initial_url.split('/')[-1]}"
    print(specified_url_kb)


