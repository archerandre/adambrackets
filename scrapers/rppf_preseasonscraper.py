# %%
import numpy as np
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import date
from kenpompy.utils import login
import os
import io

# %%
#def get_kenpom_preseason(year):
    

# %%
username = 'adamjdavis242@yahoo.com'
password = 'RoosterPom1234'
browser = login(username, password)

#url = "https://kenpom.com/fanmatch.php?d=2024-11-05"
url = "https://kenpom.com/archive.php?d=2024-11-05"

response = browser.get(url)
print(response)
soup = BeautifulSoup(response.content, 'html.parser')


# %%

# Check if the request was successful
if response.status_code == 200:
    table = soup.find("table")  # Adjust based on the table's class or id

if table is None:
        print(f"No table found")


# %%
# Step 4: Extract headers from second row of <thead>
header_rows = table.find("thead").find_all("tr")  # Get all header rows
if len(header_rows) > 1:
    header_row = header_rows[1]  # Select the second row (thead2)
else:
    header_row = header_rows[0]  # Fallback if there's only one row


# %%
#Extract the second header row (thead2)
header_rows = table.find("thead").find_all("tr")
header_row = header_rows[1] if len(header_rows) > 1 else header_rows[0]

# Get column headers and keep only the first 12 (after filtering seeds)
headers = [th.text.strip() for th in header_row.find_all("th") if "seed" not in th.get("class", [])][:12]

# Extract data rows
data = []
for row in table.find("tbody").find_all("tr"):
    cells = row.find_all("td")

    # Remove <span class="seed"> elements
    for cell in cells:
        for span in cell.find_all("span", class_="seed"):
            span.decompose()  # Completely removes the <span> element from the HTML

    # Extract clean text, remove empty strings, and keep only first 12 columns
    filtered_cells = [cell.get_text(strip=True) for cell in cells if cell.get_text(strip=True)][:12]

    # Ensure only the desired number of columns are kept
    if len(filtered_cells) == len(headers):
        data.append(filtered_cells)
    else:
        print(f"Skipping row due to column mismatch: {filtered_cells}")

# Create DataFrame
preseason_kp = pd.DataFrame(data, columns=headers)

# Display DataFrame
print(preseason_kp)


