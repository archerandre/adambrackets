# %%
import numpy as np
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from kenpompy.utils import login
import os
import io

# %% [markdown]
# # RPPF Computation Python Notebook
# ### **This notebook will serve to please the Wizard of Ball Knowledge, aka Adam "Ba11L0V3R" Davis,  @adambrackets**
# #### Author: Andre Archer, andrearcherc@gmail.com
# ------
# In this series of scripts, a few things will be done:
# - Acquiring data from Kenpom according to the RPPF ReadMe
# - Get data from Torvik 
#     - Home BARTHHAG
#     - Away-Neutral BARTHHAG
#     - Momentum ratings past Jan 31st
#     - The above will be collected for a set series of dates (Nov 1 to Day after selection Sunday)
#         - This will be to the current date for current year ratings
# - Using the README file, a dataframe will be made to compute RPPF automatically
# - Hopefully this can be used to upload to a spreadsheet
# 
# *NOTE:*
# In the current version, this is only computed for the current year, but ideally a historical database can be made to train parameters on the RPPF model
# 
# --------

# %% [markdown]
# *We need to start by setting up a few dictionaries and datasets for gathering data.*
# 
# This includes dictionaries related to dates of selection sunday and name differences.

# %%
#Get todays date
today = date.today()
today = today.strftime("%Y%m%d")  # Format the date without hyphen
#these are actually the dates one day after selection Sunday in format YYYYMMDD
selection_sunday_dates = {2015: 20150316, 
                          2016: 20160314, 
                          2017: 20170313,
                          2018: 20180312,
                          2019: 20190318, 
                          2020: 20200316, 
                          2021: 20210315, 
                          2022: 20220314, 
                          2023: 20230313, 
                          2024: 20240314,
                          2025: today}

year_start_dates =       {2015: 20141101, 
                          2016: 20151101, 
                          2017: 20161101,
                          2018: 20171101,
                          2019: 20181101, 
                          2020: 20191101, 
                          2021: 20201101, 
                          2022: 20211101, 
                          2023: 20221101, 
                          2024: 20231101,
                          2025: 20241101}
#momentum dates
momentum_start_dates = {2015: (datetime.strptime(str(20150316), "%Y%m%d") - relativedelta(months=2)).strftime("%Y%m%d"),
                        2016: (datetime.strptime(str(20160314), "%Y%m%d") - relativedelta(months=2)).strftime("%Y%m%d"),
                        2017: (datetime.strptime(str(20170313), "%Y%m%d") - relativedelta(months=2)).strftime("%Y%m%d"),
                        2018: (datetime.strptime(str(20180312), "%Y%m%d") - relativedelta(months=2)).strftime("%Y%m%d"),
                        2019: (datetime.strptime(str(20190318), "%Y%m%d") - relativedelta(months=2)).strftime("%Y%m%d"),
                        2020: (datetime.strptime(str(20200316), "%Y%m%d") - relativedelta(months=2)).strftime("%Y%m%d"),
                        2021: (datetime.strptime(str(20210315), "%Y%m%d") - relativedelta(months=2)).strftime("%Y%m%d"),
                        2022: (datetime.strptime(str(20220314), "%Y%m%d") - relativedelta(months=2)).strftime("%Y%m%d"),
                        2023: (datetime.strptime(str(20230313), "%Y%m%d") - relativedelta(months=2)).strftime("%Y%m%d"),
                        2024: (datetime.strptime(str(20240314), "%Y%m%d") - relativedelta(months=2)).strftime("%Y%m%d"),
                        2025: (datetime.today() - relativedelta(months=2)).strftime("%Y%m%d")}  #For current date

# %%
#Name Mapper
name_mapping = {
    "McNeese St.": "McNeese",
    "St. John": "St. John's",
    "Saint Peter": "Saint Peter's",
    "Saint Joseph": "Saint Joseph's",
    "Saint Mary": "Saint Mary's",
    "Mount St. Mary": "Mount St. Mary's",
    "Cal St. Northridge": "CSUN",
    "Texas A&M Commerce": "East Texas A&M",
    "Southeast Missouri St.": "Southeast Missouri",
    "UMKC": "Kansas City", 
    "SIU Edwardsville": "SIUE", 
    "Nicholls St.": "Nicholls"
}




# %% [markdown]
# *Lets start by getting the data from torvik*

# %%
#Function to grab and clean Torvik Data
def get_torvik_data(year, startyear, enddate, contype='All', venue='All'):
    url = f"https://barttorvik.com/?venue={venue}&year={year}&begin={startyear}&end={enddate}&type={contype}#"  
    print(url)  # Debugging print statement to verify correct start and end dates

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch data for venue: {venue} and year: {year}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')  # Adjust based on the table's class or id
    if table is None:
        print(f"No table found for venue: {venue}")
        return None

    # Extract all header rows (<thead>)
    header_rows = table.find('thead').find_all('tr', class_=lambda x: x != 'toprow')
        
    # Merge headers row-by-row
    headers = []
    for header_row in header_rows:
        current_row = [th.text.strip() for th in header_row.find_all('th', class_=lambda x: x != 'toprow')]
            # Extend headers to align with multi-row structure
        if len(headers) > 0:
            headers = [f"{h} | {c}" if h else c for h, c in zip(headers, current_row + [""] * (len(headers) - len(current_row)))]
        else:
            headers = current_row

    # Extract table body rows (<tbody>)
    body_rows = table.find('tbody').find_all('tr')
    data = []
    for body_row in body_rows:
        row_data = [td.text.strip() for td in body_row.find_all('td')]
    # Skip empty rows (rows that don't have any data)
        if not any(row_data):  # If the row is empty, skip it
            continue
        # Find the index of the "Team" column
        team_index = headers.index("Team")
        team_name = row_data[team_index]
        
        # Use regex to clean the team name: remove text after "vs."
        team_name = re.sub(r'(\s+vs\..*)', '', team_name).strip()  # Remove " vs." and anything after it

        team_name = re.sub(r'(\s*\((H|A)\)\s*.*)', '', team_name).strip()  # Remove text after "(H)" or "(A)"


        row_data[team_index] = team_name  # Update the team name in the row
        
        data.append(row_data)

    # Create DataFrame
    df = pd.DataFrame(data, columns=headers)

    # Ensure 'Team' column exists
    if "Team" not in df.columns:
        print("No 'Team' column found in the data.")
        return None

    # Convert 'Team' column to strings and handle missing data
    df['Team'] = df['Team'].astype(str).fillna("")

    # Extract and clean team names
    df['Team'] = (
        df['Team']
        .str.extract(r'([A-Za-z\s.&]+)'))  # Extract valid team names
    #     .fillna("")                      # Handle cases where regex extraction fails
    #     .str.strip()                     # Remove extra spaces
    #     .str.title()                     # Standardize capitalization
    # )
    return df

# %%
#What years are we looking for:
myseasons = list(range(2025,2025+1)) #must use +1 to make sure 25 is included

#Getting dataframes for torvik data
tvk_H_dict = {}
tvk_A_N_dict = {}
tvk_N_dict = {}
tvk_MOM_dict = {}
for season in myseasons:
    #PULL DATA
    tvk_data_H = get_torvik_data(venue = 'H', year = season, startyear = year_start_dates[season], enddate = selection_sunday_dates[season] ) 
    tvk_data_A_N = get_torvik_data(venue ='A-N', year = season, startyear = year_start_dates[season], enddate = selection_sunday_dates[season] ) 
    tvk_data_N = get_torvik_data(venue = 'All', year = season, startyear = year_start_dates[season], enddate = selection_sunday_dates[season], contype = 'N' ) 
    tvk_data_MOM = get_torvik_data(venue='A-N', year=season, startyear=momentum_start_dates[season], enddate=selection_sunday_dates[season])

    #Append to dictionaries
    tvk_H_dict[str(season)] = tvk_data_H
    tvk_A_N_dict[str(season)] = tvk_data_A_N
    tvk_N_dict[str(season)] = tvk_data_N
    tvk_MOM_dict[str(season)] = tvk_data_MOM

# %% [markdown]
# Now lets get current Kenpom Data

# %%
username = 'adamjdavis242@yahoo.com'
password = 'RoosterPom1234'
browser = login(username, password)
kp_dict = {}

for season in myseasons:
    
    # # File name to save the data
    # file_name = "summary%i_pt.csv" %(season%100)
    # print(file_name)
    

    if season != 2025:
        url_download = 'https://kenpom.com/getdata.php?file=summary%i_pt' %(season%100)
    else:
        url_download = 'https://kenpom.com/getdata.php?file=summary%i' %(season%100)
        
    response = browser.get(url_download)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = io.StringIO(response.text)  # Use StringIO to read the text response as a file-like object
        kp_dict[str(season)] = pd.read_csv(data)
    
    # Save the content to a file
        # with open(file_path, "wb") as file:
        #     file.write(response.content)
        # print(f"File downloaded successfully and saved to {file_path}")
        
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")

    # #Append to dictionaries
    # kp_dict[str(season)] = pd.read_csv(file_path)  # Read the CSV data into a DataFrame

# %% [markdown]
# Now we need to pull out the dataframes of interest
# 
# 

# %%
kp_df = kp_dict['2025']
tvk_H_df = tvk_H_dict['2025']
tvk_A_N_df = tvk_A_N_dict['2025']
tvk_N_df = tvk_N_dict['2025']
tvk_MOM_df = tvk_MOM_dict['2025']

# %%
kp_df.to_csv('kp_df_test.csv')
kp_df


# %%
tvk_H_df

# %%
tvk_A_N_df

# %%
tvk_N_df

# %%
tvk_MOM_df
 
# %% [markdown]
#### Next we need to make sure all the dataframs have the same names using the key from earlier

# %%
#Start by finding all names
team_names = pd.DataFrame({ 'kenpom': kp_df['TeamName'],
    'tvk_H': tvk_H_df['Team'],
    'tvk_A_N': tvk_A_N_df['Team']})
team_names = team_names.apply(lambda col: sorted(col), axis=0)
team_names.to_csv('team_names.csv')

names_in_column2_not_in_column1 = team_names['tvk_H'][~team_names['tvk_H'].isin(team_names['kenpom'])].unique()

# Find names in column 1 (`kenpom`) that do not appear in column 2 (`tvk_H`)
names_in_column1_not_in_column2 = team_names['kenpom'][~team_names['kenpom'].isin(team_names['tvk_H'])].unique()

print("Names in kenpom but not in tvk_H:")

namesdf = pd.DataFrame([names_in_column1_not_in_column2,names_in_column2_not_in_column1])
namesdf


# %% [markdown]
# Replace all these names!

# %%
tvk_A_N_df['Team']=tvk_A_N_df['Team'].replace(name_mapping)
tvk_H_df['Team']=tvk_H_df['Team'].replace(name_mapping)
tvk_N_df['Team']=tvk_N_df['Team'].replace(name_mapping)
tvk_MOM_df['Team']=tvk_MOM_df['Team'].replace(name_mapping)


# %%


# %% [markdown]
# Test again!

# %%
team_names = pd.DataFrame({ 'kenpom': kp_df['TeamName'],
    'tvk_H': tvk_H_df['Team'],
    'tvk_A_N': tvk_A_N_df['Team']})

team_names = team_names.apply(lambda col: sorted(col), axis=0)
team_names.to_csv('team_names.csv')

names_in_column2_not_in_column1 = team_names['tvk_H'][~team_names['tvk_H'].isin(team_names['kenpom'])].unique()
print("Names in tvk_H but not in kenpom:")
print(names_in_column2_not_in_column1)

# Find names in column 1 (`kenpom`) that do not appear in column 2 (`tvk_H`)
names_in_column1_not_in_column2 = team_names['kenpom'][~team_names['kenpom'].isin(team_names['tvk_H'])].unique()

print("Names in kenpom but not in tvk_H:")
print(names_in_column1_not_in_column2)

namesdf = pd.DataFrame([names_in_column1_not_in_column2,names_in_column2_not_in_column1])
namesdf

# %% [markdown]
# If the above output is an empty dataframe, that's beast. 

# %%
#putting all dataframes in alphabetical order and change tvk names to H or AN 

kp_df = kp_df.sort_values(by="TeamName")
tvk_A_N_df = tvk_A_N_df.sort_values(by="Team")
tvk_H_df = tvk_H_df.sort_values(by="Team")
tvk_N_df = tvk_N_df.sort_values(by="Team")
tvk_MOM_df = tvk_MOM_df.sort_values(by="Team")


# %%

tvk_H_df = tvk_H_df.rename(columns = {"Barthag": "Barthag-H"})
tvk_A_N_df = tvk_A_N_df.rename(columns = {"Barthag": "Barthag-AN"})
tvk_N_df = tvk_N_df.rename(columns = {"Barthag": "Barthag-N"})
tvk_MOM_df = tvk_MOM_df.rename(columns = {"Barthag": "Barthag-Mom"})

# %%
#now the index needs to be updated before concatenation
tvk_A_N_df = tvk_A_N_df.reset_index(drop = True)
tvk_H_df = tvk_H_df.reset_index(drop=True)
tvk_N_df = tvk_N_df.reset_index(drop=True)
tvk_MOM_df = tvk_MOM_df.reset_index(drop=True)
kp_df = kp_df.reset_index(drop=True)
tvk_N_df
tvk_MOM_df
# %%
kp_df

# %%
#check if tvk values line up
TVK_ALL = pd.concat(
    [tvk_H_df["Team"],
    tvk_A_N_df["Team"],
    tvk_N_df["Team"],
    tvk_MOM_df["Team"],
    pd.to_numeric(tvk_H_df["Barthag-H"]),
    pd.to_numeric(tvk_A_N_df["Barthag-AN"]),
    pd.to_numeric(tvk_N_df["Barthag-N"]),
    pd.to_numeric(tvk_MOM_df["Barthag-Mom"])],
    axis = 1, sort = False)
TVK_ALL

# %% [markdown]
# #### Getting big dataframe set up with values needed

# %%


AdamBomb = pd.concat([kp_df,
    pd.to_numeric(tvk_H_df["Barthag-H"]),
    pd.to_numeric(tvk_A_N_df["Barthag-AN"]),
    pd.to_numeric(tvk_N_df["Barthag-N"]),
    pd.to_numeric(tvk_MOM_df["Barthag-Mom"])],
    axis = 1, sort = False)
    


# %%
AdamBomb["Barthag-H Rank"] = AdamBomb["Barthag-H"].rank(ascending=False).astype(int)
AdamBomb["Barthag-AN Rank"] = AdamBomb["Barthag-AN"].rank(ascending=False).astype(int)
AdamBomb["Barthag-N Rank"] = AdamBomb["Barthag-N"].rank(ascending=False).astype(int)
AdamBomb["Barthag-Mom Rank"] = AdamBomb["Barthag-Mom"].rank(ascending=False).astype(int)
AdamBomb


# %% [markdown]
# ## Computing RPPF

# %% [markdown]
# List of original calculations done in Spreadsheet:
# 
# 1. StREM (Column S)**
# 2. StROE (Column U)**
# 3. Champion Filter (Column AG)**
# 4. Power Filter (Column AI)**
# 5. Davis Value 1 (Column AM)**
# 6. Davis Value 2 (Column AN)**
# 7. RPPF Rating (Column AO)**
# 8. Sweet 16 Index (Column AS)**
# 9. Index Rank (Column AT)** columns incorrect**

# %%
# Find Style-Relative Efficiency Margin (StREM)
def StREM(row):
    return (row["AdjOE"] - row["AdjDE"])/row["Tempo"]
AdamBomb["StREM"] = AdamBomb.apply(StREM, axis =1) 
# StREM Rank
AdamBomb["StREM Rank"] = AdamBomb["StREM"].rank(ascending=False).astype(int)

# Style-Relative Offensive Efficiency (StROE)
def StROE(row):
    return (row["AdjOE"]**2)*row["Tempo"]
AdamBomb["StROE"] = AdamBomb.apply(StROE, axis =1) 
# StROE Rank
AdamBomb["StROE Rank"] = AdamBomb["StROE"].rank(ascending=False).astype(int)
# StROE Rank
AdamBomb["StROE Rank"] = AdamBomb["StROE"].rank(ascending=False).astype(int)

def StRDE(row):
    return (row["AdjDE"]**1.6)/row["Tempo"]
AdamBomb["StRDE"] = AdamBomb.apply(StRDE, axis =1) 
# StRDE Rank
AdamBomb["StRDE Rank"] = AdamBomb["StRDE"].rank(ascending=True).astype(int)
#sort ascending = true only for this one.

def StRDEplus(row):
    return ((row["StREM Rank"] + row["StRDE Rank"])/2)
AdamBomb["StRDE+ Rank"] = AdamBomb.apply(StRDEplus, axis =1)
# StRDE+ Rank is the only StRDE+ row

# AN&H
def ANH(row):
    return ((row["Barthag-H"])+(row["Barthag-AN"])) /2 
AdamBomb["ANH"] = AdamBomb.apply(ANH, axis =1) 
# AN&H Rank
AdamBomb["ANH Rank"] = AdamBomb["ANH"].rank(ascending=False).astype(int)
# AN Rank
AdamBomb["AN Rank"] =  AdamBomb["Barthag-AN"].rank(ascending=False).astype(int)

# Non conference rank
AdamBomb["NonCon Rank"] = AdamBomb["Barthag-N"].rank(ascending=False).astype(int)

# Momentum
#added already

# Momentum Rank
AdamBomb["Mom Rank"] = AdamBomb["Barthag-Mom"].rank(ascending=False).astype(int)



# %%
#need this to check datatypes in each column for debugging
AdamBomb.dtypes

# %%
# Avg Big 6 Rank (AB5R) [(TROE Rank)+ (ANH Rank)+ (AdjOE-AdjOE)/Tempo + mom Rank + StRDE+ Rank]/6
def AB6R(row):
    return ((row['StREM Rank']+row['StROE Rank']+row['ANH Rank']+row['NonCon Rank']+row['Mom Rank']+row['StRDE+ Rank'])/6)
AdamBomb["AB6R"] = AdamBomb.apply(AB6R, axis =1)

#champfilter = (AB6R/AN)
def champfilter(row):
    return (row["AB6R"]/row["Barthag-AN"])
AdamBomb["champfilter"] = AdamBomb.apply(champfilter, axis =1)
AdamBomb["champfilter rank"] = AdamBomb["champfilter"].rank(ascending=True).astype(int)

#powerfilter = (AB6R/ANH)
def powerfilter(row):
    return (row["AB6R"]/row["ANH"])
AdamBomb["powerfilter"] = AdamBomb.apply(powerfilter, axis =1)
AdamBomb["powerfilter rank"] = AdamBomb["powerfilter"].rank(ascending=True).astype(int)



# %%
#Davis Value 1 (AN*((MIN(champfilter)/(champfilter))^(1/10))
AdamBomb["DV1"] = AdamBomb.apply(lambda row: 
    row['Barthag-AN']*(AdamBomb['champfilter'].min()/row['champfilter'])**(1/10), axis=1)
#Davis Value 2  (ANH Avg*(MIN(powerfilter)/powerfilter)^(1/8))
AdamBomb["DV2"] = AdamBomb.apply(lambda row:
    row['ANH']*(AdamBomb['powerfilter'].min()/row['powerfilter'])**(1/8), axis =1)
#RPPF VALUE ((DV1+DV2)/2)^(1/2.5)
AdamBomb["RPPF"] = AdamBomb.apply(lambda row:
    ((row["DV1"]+row["DV2"])/2)**(1/2.5), axis =1)
AdamBomb["RPPF Rank"] = AdamBomb["RPPF"].rank(ascending=False).astype(int)

#Sort by RPPF
AdamBomb = AdamBomb.sort_values(by = "RPPF Rank", ascending= True)
AdamBomb = AdamBomb.reset_index(drop = True)
#AdamBomb.to_csv("RPPF_%s.csv" %(today)) fix this for archive.
AdamBomb.to_csv("RPPF_UPDATED_RW4.csv")
AdamBomb
    

# %% [markdown]
# Checking these values against spreadsheet

# %%
powermin = AdamBomb['powerfilter'].min()
champmin = AdamBomb['champfilter'].min()
powermin, champmin

# %%


# %%



