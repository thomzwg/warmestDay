import pandas as pd
import requests
import zipfile
import os

# Download data
URI = 'https://cdn.knmi.nl/knmi/map/page/klimatologie/gegevens/daggegevens/'
FILE = 'etmgeg_260.zip'
DATABESTAND = 'etmgeg_260.txt'

try:
    response = requests.get(URI + FILE)
    response.raise_for_status()
    
    with open(FILE, 'wb') as out_file:
        out_file.write(response.content)
    
    # Unzip downloaded data
    with zipfile.ZipFile(FILE, 'r') as zip_ref:
        zip_ref.extractall()
        
    # Delete the zip file after extraction
    os.remove(FILE)
    
except requests.exceptions.RequestException as e:
    print(f"Error occurred while downloading the file: {e}")
    
except zipfile.BadZipFile as e:
    print(f"Error occurred while extracting the zip file: {e}")

# Read data, only cols DTG and TG to pandas dataframe
df = pd.read_csv(DATABESTAND, header=50, skip_blank_lines=True,
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
