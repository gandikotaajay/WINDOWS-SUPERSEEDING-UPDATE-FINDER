import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime

if len(sys.argv) != 2:
    print("Usage: python3 test-03.py <initial_url>")
    sys.exit(1)


initial_url = sys.argv[1]
response = requests.get(initial_url)
soup = BeautifulSoup(response.content, 'html.parser')
links = soup.find_all(class_='supLeftNavLink')

latest_date = None
latest_href = None

for link in links:
    date_str = link.text.split("—")[0].strip()  

    try:
        date_obj = datetime.strptime(date_str, "%B %d, %Y") 
    except ValueError:
        continue 

    if latest_date is None or date_obj > latest_date:
        latest_date = date_obj
        latest_href = link.get('href')

if latest_date:
    href_value = latest_href.split('/')[-1]
    new_url = f"https://support.microsoft.com/help/{href_value}"

else:
    new_url = initial_url

response = requests.get(new_url, allow_redirects=True)
soup = BeautifulSoup(response.content, 'html.parser')
links = soup.find_all('a')

specified_url = "https://www.catalog.update.microsoft.com/Search.aspx"
found_relevant_link = False

for link in links:
    href = link.get('href') 
    if href and href.startswith(specified_url):
        print(href)
        found_relevant_link = True

if not found_relevant_link:
    specified_url_kb = f"{specified_url}?q=KB{initial_url.split('/')[-1]}"
    print(specified_url_kb)


