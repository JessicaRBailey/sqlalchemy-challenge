# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/titanic.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurements = Base.classes.measurement
stations = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the 
    #value.  Return the JSON representation of your dictionary.

    # Query all preciptation measurements in the most recent 12 months
    most_recent_date = session.query(func.max(measurements.date)).scalar()
    one_year_earlier_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    recent_year_data = session.query(measurements.date, measurements.prcp).\
        filter(and_(measurements.date >= one_year_earlier_date, \
        measurements.date <= most_recent_date)).all()
    

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_precipitations = []
    for date, precipitation in recent_year_data:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["preciptation"] = prcp
        all_precipitations.append(precipitation_dict)

    return jsonify(all_precipitations)







if __name__ == '__main__':
    app.run(debug=True)
