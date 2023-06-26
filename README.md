# What's the warmest (or coldest) day of the week?

This python script calculates the average maximum and minimum temperatures for each day of the week (i.e. Monday, Tuesday, etc).

### Usage: ###
``` bash
python3 station_id
```
Valid station ids can be found on https://www.knmi.nl/nederland-nu/klimatologie/daggegevens. If no station id is provided, the default value of 260 will be taken. The station id 260 is De Bilt, the reference station in The Netherlands. The full data set will be used. 

### Example: ###
Let's take a look at De Bilt, station 260. The data set of this station starts at January 1, 1901.

On June 26, 2023, 
``` bash
python3 260
```
yielded the following result:
```
Mon average maximum temperature 14.0 average minimum temperature 6.3
Tue average maximum temperature 13.8 average minimum temperature 6.3
Wed average maximum temperature 13.8 average minimum temperature 6.3
Thu average maximum temperature 13.9 average minimum temperature 6.3
Fri average maximum temperature 13.8 average minimum temperature 6.3
Sat average maximum temperature 13.9 average minimum temperature 6.3
Sun average maximum temperature 13.9 average minimum temperature 6.3
```
So, for some reason Monday is the warmest day of the week in De Bilt! It's very likely that's a coincedence.
