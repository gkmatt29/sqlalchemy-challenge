import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation:<br/>"
        f"/api/v1.0/stations:<br/>"
        f"/api/v1.0/tobs:<br/>"
        f"/api/v1.0/<start>:<br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    session = Session(engine)
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    return jsonify(precipitation_results)

@app.route("/api/v1.0/stations")
def prcp():
    session = Session(engine)
    stations = session.query(Station.name).all()
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    tobs_results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.station == 'USC00518838').group_by(Measurement.station).all()
    return jsonify(tobs_results)


@app.route("/api/v1.0/<start>")
def start():
    session = Session(engine)
    summary = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= '2016-08-01').group_by(Measurement.station).all()
    return jsonify(summary)


if __name__ == '__main__':
    app.run(debug=True)
