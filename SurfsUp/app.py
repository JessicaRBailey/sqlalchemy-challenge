# Import the dependencies.
import os
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, func, and_

from flask import Flask, jsonify, request, g


#################################################
# Database Setup
#################################################
sqlpath = os.path.abspath("C:/Users/Jessi/Desktop/Data Analytics Bootcamp/Challenges/Challenge_10/sqlalchemy-challenge/SurfsUp/Resources/hawaii.sqlite")
engine = create_engine(f"sqlite:///{sqlpath}")  #Resources\hawaii.sqlite

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurements = Base.classes.measurement
stations = Base.classes.station

# Create our session (link) from Python to the DB
# session = Session(engine)
SessionClass = sessionmaker(bind=engine)
session = SessionClass()

def get_date_ranges():
    most_recent_date = session.query(func.max(measurements.date)).scalar()
    most_recent_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d')  # Convert to datetime
    one_year_earlier_date = most_recent_date - dt.timedelta(days=365)
    return most_recent_date, one_year_earlier_date


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Before each request, set the session to the global 'g' object (help from chatgpt)
@app.before_request
def before_request():
    g.session = session

# After each request, close the session
@app.teardown_request
def teardown_request(exception=None):
    if hasattr(g, 'session'):
        g.session.close()


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/DATE  Replace 'DATE' with your own date in the format year-month-day.  For example, /api/v1.0/2010-1-16.<br/>"
        f"/api/v1.0/DATE/DATE  Replace each 'DATE' with your own start and end dates in the format year-month-day.  For example, /api/v1.0/2011-9-1/2012-8-7.<br/>"
    )

#################################################
# Preciptation JSON Route
#################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    most_recent_date, one_year_earlier_date = get_date_ranges()

    recent_year_data = g.session.query(measurements.date, measurements.prcp).\
        filter(and_(measurements.date >= one_year_earlier_date,
                    measurements.date <= most_recent_date)).all()

    all_precipitations = []
    for date, prcp in recent_year_data:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["precipitation"] = prcp
        all_precipitations.append(precipitation_dict)

    return jsonify(all_precipitations)

#################################################
# Stations JSON Route
#################################################

@app.route("/api/v1.0/stations")
def get_stations():

    # Query all stations
    station_query = g.session.query(stations).all()

    # Create a list of dictionaries for all stations
    all_stations = []
    for station in station_query:
        station_dict = {}
        station_dict["station"] = station.station
        station_dict["name"] = station.name
        all_stations.append(station_dict)

    return jsonify(all_stations)

#################################################
# Temperature JSON Route
#################################################

@app.route("/api/v1.0/tobs")
def temperature():
    most_recent_date, one_year_earlier_date = get_date_ranges()

    recent_year_temps = g.session.query(measurements.date, measurements.tobs).\
        filter(and_(measurements.date >= one_year_earlier_date,
                    measurements.date <= most_recent_date)).all()

    all_temperatures = []
    for date, tobs in recent_year_temps:
        temperature_dict = {}
        temperature_dict["date"] = date
        temperature_dict["temperature"] = tobs
        all_temperatures.append(temperature_dict)

    return jsonify(all_temperatures)


#################################################
# Start Date JSON Route
#################################################

@app.route("/api/v1.0/<start>")
def temp_stats1(start):
    most_recent_date, one_year_earlier_date = get_date_ranges()
    
    # Convert the user-provided date to a datetime object
    user_selected_date = dt.datetime.strptime(start, '%Y-%m-%d')
    
    # Check if the user-selected date is outside the valid range
    if user_selected_date < dt.datetime(2010, 1, 1) or user_selected_date > most_recent_date:
        return jsonify({"error": "Please select a date between 2010-01-01 and " + str(most_recent_date)})

    # Collect data from the date range
    temps_from_date = g.session.query(measurements.date, measurements.tobs).\
        filter(and_(measurements.date >= user_selected_date,
                    measurements.date <= most_recent_date)).all()
        
    # Calculate min, max, and avg for the station with the most observations
    most_observed_station = 'USC00519281'
    TMIN = session.query(func.min(measurements.tobs)).\
        filter(and_(measurements.station == most_observed_station,
                    measurements.date >= user_selected_date,
                    measurements.date <= most_recent_date)).\
        first()
    TMAX = session.query(func.max(measurements.tobs)).\
        filter(and_(measurements.station == most_observed_station,
                    measurements.date >= user_selected_date,
                    measurements.date <= most_recent_date)).\
        first()
    TAVG = session.query(func.avg(measurements.tobs)).\
        filter(and_(measurements.station == most_observed_station,
                    measurements.date >= user_selected_date,
                    measurements.date <= most_recent_date)).\
        first()
    
    # Add them to a dictionary to prep them for JSON format and display
    most_active_station_temps = {
        "Minimum Temperature": TMIN[0] if TMIN else None,
        "Maximum Temperature": TMAX[0] if TMAX else None,
        "Average Temperature": TAVG[0] if TAVG else None
    }

    return jsonify(most_active_station_temps)

#################################################
# Start and End Date JSON Route
#################################################

@app.route("/api/v1.0/<start>/<end>")
def temp_stats2(start,end):
    most_recent_date, one_year_earlier_date = get_date_ranges()
    
    # Convert the user-provided date to a datetime object
    user_selected_start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    user_selected_end_date = dt.datetime.strptime(end, '%Y-%m-%d')
    
    # Check if the user-selected date is outside the valid range
    if user_selected_start_date < dt.datetime(2010, 1, 1) or user_selected_start_date > most_recent_date:
        return jsonify({"error": "Please select a date between 2010-01-01 and " + str(most_recent_date)})
    if user_selected_end_date < dt.datetime(2010, 1, 1) or user_selected_end_date > most_recent_date:
        return jsonify({"error": "Please select a date between 2010-01-01 and " + str(most_recent_date)})
    if user_selected_start_date > user_selected_end_date:
        return jsonify({"error": "Please ensure the start date is before or equal to the end date."})

    # Collect data from the date range
    temps_from_date = g.session.query(measurements.date, measurements.tobs).\
        filter(and_(measurements.date >= user_selected_start_date,
                    measurements.date <= user_selected_end_date)).all()
        
    # Calculate min, max, and avg for the station with the most observations
    most_observed_station = 'USC00519281'
    TMIN = session.query(func.min(measurements.tobs)).\
        filter(and_(measurements.station == most_observed_station,
                    measurements.date >= user_selected_start_date,
                    measurements.date <= user_selected_end_date)).\
        first()
    TMAX = session.query(func.max(measurements.tobs)).\
        filter(and_(measurements.station == most_observed_station,
                    measurements.date >= user_selected_start_date,
                    measurements.date <= user_selected_end_date)).\
        first()
    TAVG = session.query(func.avg(measurements.tobs)).\
        filter(and_(measurements.station == most_observed_station,
                    measurements.date >= user_selected_start_date,
                    measurements.date <= user_selected_end_date)).\
        first()
    
    # Add them to a dictionary to prep them for JSON format and display
    most_active_station_temps = {
        "Minimum Temperature": TMIN[0] if TMIN else None,
        "Maximum Temperature": TMAX[0] if TMAX else None,
        "Average Temperature": TAVG[0] if TAVG else None
    }

    return jsonify(most_active_station_temps)



if __name__ == '__main__':
    app.run(debug=True)
