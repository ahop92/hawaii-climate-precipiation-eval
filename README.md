# Hawaii Precipiation and Cimate Analysis/Evaluation

## Background

Given climate/weather data specific to the state Hawaii, the goal of this study is to use Python and SQLAlchemy to do basic climate analysis and data exploration about various weather stations in the state. This analysis makes use of the following Python libraries: SQLAlchemy ORM queries, Pandas, and Matplotlib.

In all sections of this analysis the following ORM approach was used to extract information from the employed sqllite database: 

1. Establish a connection using create_engine from the SQLAlchemy library 
2. Manipulate the automap_base() function in order to establish objects for the attributes of the data. 
3. Using the Base class, extract the classes present within the database and identify all of the keys associated with the class
    A. In this case, the primary classes identified by the ORM were 'measurement' and 'station'
4. Lastly, establish a session with the database to use the identified classes to perform queries. 
    A. In the case of the app.py file, this was done on a route per route basis. 
    B. In the case of the climate_starter.ipynb file, one session was established for the whole notebook. 

![image](https://raw.github.com/ahop92/hawaii-climate-precipiation-eval/main/images/jupyterSQLAlchemyoverview.PNG)


### Precipitation Analysis

The goal of this section was to provide an overall precipitation analysis over all stations present in the database using the following steps:

1. Find the most recent date in the data set.

![image](https://raw.github.com/ahop92/hawaii-climate-precipiation-eval/main/images/recentdate.PNG)

2. Using the date found in #1, calculate the date exactly one year prior. This was accomplished by transforming the date to a datetime object, completing the math using the timedelta function, and then transforming the calculated value to a string to be used in the subsequent queries.

![image](https://raw.github.com/ahop92/hawaii-climate-precipiation-eval/main/images/1yearprior.PNG)

3. Using the dates identified above, select only the `date` and `prcp` values.

4. Load the query results into a Pandas DataFrame and set the index to the date column.

5. Sort the DataFrame values by `date`.

![image](https://raw.github.com/ahop92/hawaii-climate-precipiation-eval/main/images/jupyterSQLAlchemyoverview.PNG)

6. Plot the results using the DataFrame `plot` method.

![image](https://raw.github.com/ahop92/hawaii-climate-precipiation-eval/main/images/prcpgraph.PNG)

7. Use Pandas to print the summary statistics for the precipitation data.

![image](https://raw.github.com/ahop92/hawaii-climate-precipiation-eval/main/images/summarystats.PNG)


### Station Analysis
The goal of this section was to provide an overall precipitation analysis by station in the database using the following steps:

1. Design a query to calculate the total number of stations in the dataset. This was accomplished using the Stations class/table. 

2. Design a query to find the most active stations by counting the number of times each station appeared in the Measurement class/table

3. List the stations and observation counts in descending order and extract the highest ranking station to use for other queries. 

![image](https://raw.github.com/ahop92/hawaii-climate-precipiation-eval/main/images/stationoverview.PNG)

4. Using the output from #3, calculate the lowest, highest, and average temperature.

![image](https://raw.github.com/ahop92/hawaii-climate-precipiation-eval/main/images/highestlowestaverage.PNG)

5. Design a query to retrieve the last 12 months of temperature observation data (TOBS) for the station with the highest number of appearances.

![image](https://raw.github.com/ahop92/hawaii-climate-precipiation-eval/main/images/TOBS.PNG)




- - -

## Climate App

With the numerical analysis and visualizations complete, the app.py file was created to allow users to request information from the Hawaii database with API style deployment using the following approach: 

1. A home page was created to show the user all of the routes they can use to retrieve information from the database. 

![image](https://raw.github.com/ahop92/hawaii-climate-precipiation-eval/main/images/pageoverview.PNG)

2. A route was created to pull the general precipitation data associated with each date. 

![image](https://raw.github.com/ahop92/hawaii-climate-precipiation-eval/main/images/prcpdict.PNG)

3. A route was created to pull the basic information about each station.

![image](https://raw.github.com/ahop92/hawaii-climate-precipiation-eval/main/images/stationjson.PNG)

3. A route was created to pull the TOBS information for the most active station. 

![image](https://raw.github.com/ahop92/hawaii-climate-precipiation-eval/main/images/tobsjson.PNG)

4. A route was created to pull a statistical analysis on the TOBS information for anything greater than or equal to the user entered start date. 

![image](https://raw.github.com/ahop92/hawaii-climate-precipiation-eval/main/images/dateusecase.PNG)

![image](https://raw.github.com/ahop92/hawaii-climate-precipiation-eval/main/images/dateuseresult.PNG)

5. A route was created to pull a statistical analysis on the TOBS information for anything in between the user entered start and end dates, inclusive. 

![image](https://raw.github.com/ahop92/hawaii-climate-precipiation-eval/main/images/statisticsusecase.PNG)

![image](https://raw.github.com/ahop92/hawaii-climate-precipiation-eval/main/images/statisticsusecaseresults.PNG)


The user is instructed to access the API using the following directions 

Please append either of the routes onto the ending of the address used to deploy this app.

For example, if using a local production server such as 127.0.0.1:5000
you would write `127.0.0.1:5000/api/v1.0/precipitation` to view all of the
precipitation data offered by this API.

For the start date and end date routes: please offer dates in YYYY-MM-DD format.


All of the output information is offered in JSON format. 

