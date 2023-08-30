# sqlalchemy-challenge
Challenge 10

In this exercise we evaluate the measurements taken at 9 weather stations in Hawaii.  

In the jupyter notebook "climate_analysis.ipynb" we use sqlalchemy to read a sqlite database with two tables, one with weather readings and one with station details.  After we explore the contents of the database, we filter out the precipitation readings for the last 12 months recorded, and graph them on a bar chart.  Last, we determined which station had the most recorded observations and used only that stations data to plot the frequency of temperatures recorded over the same 12 month period in 12 bins.  A join of the two tables helped us name the chart using the station name rather than its ID number.

Next, we created an app to display json data based on the user's preferences.  The user can review all the preciptation data for the past 12 months, the station names and ids, the temperatures for the past 12 months at the Waihee station, or the min, max, and average temperatures at Waihee given a start date or a start and end date.  

What we can see from these data is that Hawaii temperatures range between a comfortable 60-85 degrees year round and that it can rain close to 7 inches per day on some days of the year.  
