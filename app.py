#Introduce necessary imports
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
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
        f"Hi there! Here are your available routes to explore the recorded weather information for weather bases in Hawaii API.<br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<start><br/>"
        f"/api/v1.0/start<start>/end<end><br/><br/><br/>"
        f"For the start date and end date routes: please offer dates in YYYY-MM-DD format."
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

    session = Session(engine)
    station_query = session.query(Stations.name, Stations.id, Stations.longitude, Stations.elevation, Stations.station, Stations.latitude).all()
    session.close()

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

    holder = 0 


@app.route("/api/v1.0/<start>")
def start_only():

    holder = 0 


@app.route("/api/v1.0/<start>/<end>")
def start_and_end():

    holder = 0 


# Define main behavior
if __name__ == "__main__":
    app.run(debug=True)

