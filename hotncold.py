''' This script calculates the average maximum and minimum temperatures for 
each day of the week.

usage: python3 station_id

Valid station ids can be found on
https://www.knmi.nl/nederland-nu/klimatologie/daggegevens

Default value = 260 (De Bilt, which is the reference station in NL)

June 26, 2023, by Thom Zwagers
'''

import os
import sys
import requests
import pandas as pd
import zipfile

# read argument from command line, 2nd arg = station id, default = 260
try:
    station_id = sys.argv[1]
except IndexError:
    station_id = 260

# Download data
URI = 'https://cdn.knmi.nl/knmi/map/page/klimatologie/gegevens/daggegevens/'
bestand = f"etmgeg_{station_id}.zip"
databestand = f"etmgeg_{station_id}.txt"

try:
    response = requests.get(URI + bestand)
    response.raise_for_status()
    
    with open(bestand, 'wb') as out_file:
        out_file.write(response.content)
    
    # Unzip downloaded data
    with zipfile.ZipFile(bestand, 'r') as zip_ref:
        zip_ref.extractall()
        
    # Delete the zip file after extraction
    os.remove(bestand)
    
except requests.exceptions.RequestException as e:
    print(f"Error occurred while downloading the file: {e}")
    
except zipfile.BadZipFile as e:
    print(f"Error occurred while extracting the zip file: {e}")

# Read data, only cols DTG and TG to pandas dataframe
df = pd.read_csv(databestand, header=50, skip_blank_lines=True,
                 skipinitialspace=True, usecols=['YYYYMMDD', 'TG', 'TX', 'TN'])

# Create extra column with weekday (0 = Monday, 1 = Tuesday, ..., 6 = Sunday)
df['weekday'] = pd.to_datetime(df['YYYYMMDD'], format='%Y%m%d').dt.dayofweek

# Compute mean values per weekday
WEEKDAYS = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
for weekday_number, weekday in enumerate(WEEKDAYS):
    avgTX = (df[df['weekday'] == weekday_number]['TX'].mean() / 10).round(1)
    avgTN = (df[df['weekday'] == weekday_number]['TN'].mean() / 10).round(1)

    print(f"{weekday} average maximum temperature {avgTX} "
          f"average minimum temperature {avgTN}")
