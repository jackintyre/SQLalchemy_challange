import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

        # Database 
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)


        #create app menu
@app.route("/")
def Main():
    
    return (
        f"/api/v1.0/Precipitation<br/>"
        f"/api/v1.0/Stations<br/>"
        f"/api/v1.0/Tobs<br/>"
        f"/api/v1.0/[Start]<br/>"
        f"/api/v1.0/[Start ]/[End]<br/>"
    )
        #Precipitation Query
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)
    """Precipitation Data"""
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-24").\
        all()

    session.close()


    all_prcp = []
    for date,prcp  in results:
        prcp = {}
        prcp["date"] = date
        prcp["prcp"] = prcp
               
        all_prcp.append(prcp)

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)

    """Return a list of all Stations"""
    
    results = session.query(Station.station).\
                 order_by(Station.station).all()

    session.close()

    
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)

    """Return a list of all TOBs"""
   

    results = session.query(Measurement.date,  Measurement.tobs,Measurement.prcp).\
                filter(Measurement.date >= '2016-08-23').\
                filter(Measurement.station=='USC00519281').\
                order_by(Measurement.date).all()

    session.close()

    all_tobs = []
    for prcp, date,tobs in results:
        tobs_dict = {}
        tobs_dict["prcp"] = prcp
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

    
@app.route("/api/v1.0/<start>")
def Start_date(start):
    
    session = Session(engine)

    """Return a list of min, avg and max tobs for a start date"""

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).all()

    session.close()

    start_date = []
    for min, avg, max in results:
        start = {}
        start["min_temp"] = min
        start["avg_temp"] = avg
        start["max_temp"] = max
        start_date.append(start) 
    return jsonify(start_date)

@app.route("/api/v1.0/<start_date>/<end_date>")
def Start_end_date(start, end):
    
    session = Session(engine)

    """Return a list of min, avg and max tobs for start and end dates"""

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()
  
    end_tobs = []
    for min, avg, max in results:
        end = {}
        end["min_temp"] = min
        end["avg_temp"] = avg
        end["max_temp"] = max
        end_tobs.append(end) 
    
    return jsonify(end_tobs)

if __name__ == "__main__":
    app.run(debug=True)