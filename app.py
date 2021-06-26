# Import dependencies

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

# Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine,reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask setup
app = Flask(__name__)

# Routes
@app.route("/")
def home():
    return (
        f"<h2>How's the weather in Hawaii?</h2><br/>" 
        f"<h3><i>Let's find out with this API!</i></h3><br/><br/>"
        f"<h4>Available Routes:</h4><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    session = Session(engine)
    year_ago = dt.datetime(2017,8,23) - dt.timedelta(days=365)
    last_12 = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>year_ago).all()
    session.close()
    
    return jsonify(dict(last_12))


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = session.query(Station.station).distinct().all()
    session.close()
    list_stations = list(np.ravel(stations))

    return jsonify(list_stations)



@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    year_ago = dt.datetime(2017,8,23) - dt.timedelta(days=365)
    last_12_temps = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>year_ago).all()
    session.close()
    list_temps = list(np.ravel(last_12_temps))



# @app.route("/api/v1.0/<start>")
# def start():

# @app.route("/api/v1.0/<start>/<end>")
# def end():

if __name__ == "__main__":
    app.run(debug=True)