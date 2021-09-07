# Hawaii Precipiation and Cimate Analysis/Evaluation

## Background

Given climate/weather data specific to the state Hawaii, the goal of this challenge is to use Python and SQLAlchemy to do basic climate analysis and data exploration. This analysis has an emphasized focus on manipualting the following libraries: SQLAlchemy ORM queries, Pandas, and Matplotlib.

In all sections of this analysis the following ORM approach was used to extract information from the offered database: 

1. Establish a connection with the SQLite database using create_engine from the SQLAlchemy library 
2. Manipulate the automap_base() function. 
3. Then, using the Base class, extract the classes present within the database and identify all of the keys associated with the class
    A. In this case, the primary classes identified by the ORM were 'measurement' and 'station'
4. Lastly, establish a session with the database to use the identified classes to perform queries. 
    A. In the case of the app.py file, this was done on a route per route basis. 
    B. In the case of the climate_starter.ipynb file, one session was established for the whole notebook. 


### Precipitation Analysis

The goal of this section was to provide an overall precipitation analysis over all stations present in the database using the following steps:

1. Find the most recent date in the data set.
2. Using the date found in #1, calculate the date exactly one year prior. This was accomplished by transforming the date to a datetime object, completing the math using the timedelta function, and then transforming the calculated value to a string to be used in the subsequent queries.
3. Using the dates identified above, select only the `date` and `prcp` values.
4. Load the query results into a Pandas DataFrame and set the index to the date column.
5. Sort the DataFrame values by `date`.
6. Plot the results using the DataFrame `plot` method.
7. Use Pandas to print the summary statistics for the precipitation data.

A bar plot visualization can be found for an overall analysis of precipitation data for all of the stations in the jupyter notebook.

### Station Analysis
The goal of this section was to provide an overall precipitation analysis over all stations present in the database using the following steps:

1. Design a query to calculate the total number of stations in the dataset. This was accomplished using the Stations class/table. 
2. Design a query to find the most active stations by counting the number of times each station appeared in the Measurement class/table
3. List the stations and observation counts in descending order and extract the highest ranking station to use for other queries. 
4. Using the output from #3, calculate the lowest, highest, and average temperature.
5. Design a query to retrieve the last 12 months of temperature observation data (TOBS) for the station with the highest number of appearances.

A histogram analysis of the temperature data can be found in the jupyter notebook. 

- - -

## Climate App

With the numerical analysis and visualizations complete, the app.py file was created to allow users to request information from the Hawaii database with API style deployment using the following approach: 

1. A home page was created to show the user all of the routes they can use to retrieve information from the database. 
2. A route was created to pull the general precipitation data associated with each date. 
3. A route was created to pull the TOBS information for the most active station. 
4. A route was created to pull a statistical analysis on the TOBS information for anything greater than or equal to the user entered start date. 
5. A route was created to pull a statistical analysis on the TOBS information for anything in between the user entered start and end dates, inclusive. 


All of the output information was offered in JSON format. 

