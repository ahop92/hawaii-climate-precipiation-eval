#Introduce necessary imports
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


#Create engine to connect with sqlite database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Reflect the existing database into a new model
Base = automap_base()

#Reflect tables from the database into the model
Base.prepare(engine, reflect=True)

#Define class objects that can be used to extract data from the database using the ORM
Measurements = Base.classes.measurement
Stations = Base.classes.station

#Create app and pass name class
app = Flask(__name__)


#Define index/main page operation
@app.route("/")
def welcome():

    """List all available api routes."""
    return (
        f"Hi there! Welcome to the Hawaii precipiation and station API. Please browse the different options for data using the routes specified below.<br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/YYYY-MM-DD<br/>"
        f"/api/v1.0/start/YYYY-MM-DD/end/YYYY-MM-DD<br/><br/><br/>"
        f"<b>General Instructions:</b><br><br> Please append either of the routes onto the ending of the address used to deploy this app.<br><br> For example, if using a local production server such as 127.0.0.1:5000<br/>"
        f"you would write `127.0.0.1:5000/api/v1.0/precipitation` to view all of the<br> precipitation data offered by this API."
        f"<br><br>For the start date and end date routes: please offer dates in YYYY-MM-DD format."
    )


#Define precipiation page operation
@app.route("/api/v1.0/precipitation")
def prcp():

    """Convert the query results to a dictionary using date as the key and prcp as the value."""
    """Return the JSON representation of your dictionary."""

    #Create session link to sqlite database
    session = Session(engine)
    precipitation_query = session.query(Measurements.date, Measurements.prcp).all()
    session.close()

    #Create corresponding dictonary for user
    prcp_dict = {}

    for date, precipitation_value in precipitation_query: 
        prcp_dict[date] = precipitation_value

    return (jsonify(prcp_dict))


@app.route("/api/v1.0/stations")
def st():

    #Create session link to sqlite database and query all information about the stations in Hawaii 
    session = Session(engine)
    station_query = session.query(Stations.name, Stations.id, Stations.longitude, Stations.elevation, Stations.station, Stations.latitude).all()
    session.close()

    #Append information retrieved from query into a list of dictionaries, then add JSON format to output
    station_list = []
    for name, id, longitude, elevation, station, latitude in station_query:
        station_dict = {}
        station_dict["name"] = name
        station_dict["id"] = id
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        station_dict["station"] = station
        station_dict["latitude"] = latitude
        station_list.append(station_dict)

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():

    #Create a link with the sqlite database and query the count of each station in the measurement data
    session = Session(engine)
    activestations_query = session.query(Measurements.station, func.count(Measurements.station)).\
        group_by(Measurements.station).\
        order_by(func.count(Measurements.station).desc()).all()

    #Query the the date data from the measurement data to identify the final date present in the database
    query_enddate = session.query(Measurements.date).order_by(Measurements.date.desc()).first()
    session.close()
    
    #Based on the date identifies in query_enddate, convert that value to a datetime object and complete datetime arithmetic to identify exactly one year before the enddate
    #Then, convert the start date from a datetime object to a string so that it can be used in queries
    #Note: The date and time information should focus on the last year present in the dataset
    query_startdate = dt.datetime.strftime(dt.datetime.strptime(query_enddate[0], '%Y-%m-%d') - dt.timedelta(days=365), '%Y-%m-%d')
    max_activestation = activestations_query[0]

    #Initiate new session with database to complete the TOBS query for the most active station between the start and end dates identified
    session = Session(engine)
    tob_mostactive_query = session.query(Measurements.date, Measurements.tobs).\
                    filter(Measurements.date >= query_startdate).\
                    filter(Measurements.date <= query_enddate[0]).\
                    filter(Measurements.station == max_activestation[0]).\
                    order_by(Measurements.date.desc()).all()
    session.close()

    #Append the information retrieved form the query into a list of dictionaries and then return jsonified data
    tobs_list = []
    for date, tobs in tob_mostactive_query:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

@app.route("/api/v1.0/start/<start>")
def start_only(start):

    #Establish boolean to check for invalid data entry to API URL
    run_query = False

    #Extract all date information for logical comparison to date entered in URL 
    session = Session(engine)
    date_check = session.query(Measurements.date).all()
    session.close()

    #If date idenitified exists in dataset, allow the value to be passed through to the query
    for date in date_check:
        if date[0] == start:
            run_query = True

    #Extract max TOBs, min TOBS, and average TOBS from all dates greater than and including the entered start date 
    if run_query == True:
        session = Session(engine)
        date_and_tob = session.query(Measurements.date, func.min(Measurements.tobs), func.max(Measurements.tobs), func.avg(Measurements.tobs)).\
                            filter(Measurements.date >= start).all()
        session.close()

        #Append the retrieved information to a list of dictionaries and jsonify the output
        tob_stats_list = []
        for date, tmin, tmax, tavg in date_and_tob:
            tobs_stats_dict = {}
            tobs_stats_dict = {"Query Start Date": date, "Min TOB": tmin, "Max TOB": tmax, "Average TOB": tavg }
            tob_stats_list.append(tobs_stats_dict)

        return jsonify(tob_stats_list)

    #If the date entered does not exist, return error message in json format
    return jsonify({"Error": f"We do not have weather data for {start}."}), 404

@app.route("/api/v1.0/start/<start>/end/<end>")
def start_and_end(start, end):

    #Establish boolean to check for invalid data entry to API URL for start and end date
    start_query = False
    end_query = False

    #Extract all date information for logical comparison to date entered in URL
    session = Session(engine)
    date_check = session.query(Measurements.date).all()
    session.close()

    #If dates idenitified exists in dataset, allow the values to be passed through to the query
    for date in date_check:
        if (date[0] == start):
            start_query = True

        if (date[0] == end):
            end_query = True

    #Extract max TOBs, min TOBS, and average TOBS from all dates between the start and end dates, inclusive. 
    if (start_query == True) and (end_query == True):
        session = Session(engine)
        date_and_tob = session.query(Measurements.date, func.min(Measurements.tobs), func.max(Measurements.tobs), func.avg(Measurements.tobs)).\
                            filter(Measurements.date >= start).\
                            filter(Measurements.date <= end).all()
        session.close()

        #Append the retrieved information to a list of dictionaries and jsonify the output
        tob_stats_list = []
        for date, tmin, tmax, tavg in date_and_tob:
            tobs_stats_dict = {}
            tobs_stats_dict = {"Query Start Date": date, "Min TOB": tmin, "Max TOB": tmax, "Average TOB": tavg }
            tob_stats_list.append(tobs_stats_dict)

        return jsonify(tob_stats_list)
    
    #If statement set to return errors depending on which date (start or end) was identified as missing from the dataset
    elif (start_query == False) and (end_query == True):
        return jsonify({"Error": f"We do not have weather data for {start}."}), 404
    elif (start_query == True) and (end_query == False):
        return jsonify({"Error": f"We do not have weather data for {end}."}), 404
    else: 
        return jsonify({"Error": f"We do not have weather data for either {start} or {end}."}), 404



# Define main behavior
if __name__ == "__main__":
    app.run(debug=True)

