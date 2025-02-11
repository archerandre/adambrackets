"""
Torvik Preseason Scaper
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_barttorvik(year):
    # URL for the given year
    url = f"https://barttorvik.com/trank-time-machine.php?year={year}"

    # Send GET request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Locate the table
        table = soup.find("table")

        if table is None:
            print(f"No table found for year {year}.")
            return

        # Extract rows of the table
        rows = table.find_all("tr")[1:]  # Skip the header row

        data = []
        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 9:  # Ensure the row has at least 9 columns
                team = cells[1].text.strip()  # Column 2: Team
                barthag = cells[8].text.strip()  # Column 9: BARTHAG

                # Append the data
                data.append({"Year": year, "Team": team, "BARTHAG": barthag})

        # Save to CSV
        df = pd.DataFrame(data)
        df.to_csv(f"barttorvik_{year}.csv", index=False)
        print(f"Data scraping complete for {year}! Saved to barttorvik_{year}.csv")
    else:
        print(f"Failed to retrieve data for year {year}. HTTP Status Code: {response.status_code}")

# Loop over years from 2015 to 2024
for year in range(2015, 2025):
    scrape_barttorvik(year)
