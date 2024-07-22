# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template

#################################################
# Database Setup
#################################################
engine = create_engine("postgresql://postgres:postgres@localhost:5432/bart_train_routes")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
bart_advisories = Base.classes.bart_advisories
bart_crime = Base.classes.bart_crime_report_2021
bart_route_info = Base.classes.bart_route_info
bart_routes = Base.classes.bart_routes
bart_stations = Base.classes.bart_station_info

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################


# creating welcome page
# creating welcome page
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/data_docs")
def data_docs():
    return """Welcome to the BART Train Routes API! This will inform you about !<br/>
        Available Routes:<br/>
        /api/v1.0/advisories<br/>
        /api/v1.0/crime_reports<br/>
        /api/v1.0/route_info<br/>
        /api/v1.0/stations<br/>
        """


@app.route("/api/v1.0/advisories")
def advisories():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query all advisories
    results = session.query(bart_advisories.id, bart_advisories.station, bart_advisories.description, bart_advisories.date, bart_advisories.time).all()
    # Create a dictionary from the row data and append to a list of all_advisories
    all_advisories = []
    for id, station, description, date, time in results:
        advisory_dict = {}
        advisory_dict["ID"] = id
        advisory_dict["Station"] = station
        advisory_dict["Description"] = description
        advisory_dict["Date"] = date
        advisory_dict["Time"] = time
        all_advisories.append(advisory_dict)
    session.close()
    return jsonify(all_advisories)


@app.route("/api/v1.0/crime_reports")
def crime_reports():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(bart_crime.id, bart_crime.location, bart_crime.date, bart_crime.time, bart_crime.charge_description)
    all_crime_reports = []
    for id, location, date, time, charge_description in results:
        crime_dict = {}
        crime_dict["ID"] = id
        crime_dict["Location"] = location
        crime_dict["Charge Description"] = charge_description
        crime_dict["Date"] = date
        crime_dict["Time"] = time
        all_crime_reports.append(crime_dict)
    session.close()
    return jsonify(all_crime_reports)


@app.route("/api/v1.0/crime_count_<station_id>")
def crime_count(station_id):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    station_name = session.query(bart_stations.name).filter(bart_stations.id == station_id).first()[0]
    print(station_name)
    results = session.query(bart_crime.charge_description, func.count(bart_crime.id)).filter(bart_crime.location.like("%" + station_name + "%")).group_by(bart_crime.charge_description).order_by(func.count(bart_crime.id).desc()).limit(5).all()
    # bart_crime.location == station_name).
    results = [{"desc": row[0], "count": row[1]} for row in results]
    session.close()
    return jsonify(results)


@app.route("/api/v1.0/route_info")
def route_info():
    session = Session(engine)
    # Query all route info
    results = session.query(bart_route_info.id, bart_route_info.route_id, bart_route_info.name, bart_route_info.abbr, bart_route_info.color, bart_route_info.config).all()
    # Create a dictionary from the row data and append to a list of all_route_info
    all_route_info = []
    for id, route_id, name, abbr, color, config in results:
        route_dict = {}
        route_dict["ID"] = id
        route_dict["Route ID"] = route_id
        route_dict["Name"] = name
        route_dict["Abbreviation"] = abbr
        route_dict["Color"] = color
        route_dict["Config"] = config
        all_route_info.append(route_dict)
    session.close()
    return jsonify(all_route_info)


# @app.route('/api/v1.0/routes')
# def routes():
#     session=Session(engine)
#     # Query all route
#     results = session.query(bart_routes.routes, bart_routes.id, bart_routes.route_id, bart_routes.routes_name,bart_routes.route.abbr, bart_routes.routes_color, bart_routes.routes_config).all()

#     # Create a dictionary from the row data and append to a list of all_route_info
#     all_routes = []
#     for routes, id, route_id, route_name, route_abbr, route_color, route_config in results:
#         route_dict = {}
#         route_dict["Routes"] = routes
#         route_dict["ID"] = id
#         route_dict["Route ID"] = route_id
#         route_dict["Route Name"] = route_name
#         route_dict["Route Abbreviation"] = route_abbr
#         route_dict["Route Color"] = route_color
#         route_dict["Route Config"] = route_config
#         all_routes.append(route_dict)
#     session.close()
#     return jsonify(all_routes)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    # Query all stations
    results = session.query(bart_stations.id, bart_stations.name, bart_stations.abbr, bart_stations.latitude, bart_stations.longitude, bart_stations.address, bart_stations.city, bart_stations.zipcode).all()
    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for id, name, abbr, latitude, longitude, bart_address, city, zipcode in results:
        station_dict = {}
        station_dict["ID"] = id
        station_dict["Name"] = name
        station_dict["Abbreviation"] = abbr
        station_dict["Latitude"] = latitude
        station_dict["Longitude"] = longitude
        station_dict["BART Address"] = bart_address
        station_dict["City"] = city
        station_dict["Zipcode"] = zipcode
        all_stations.append(station_dict)

        # all_stations=[{'station id':station_id,}for station_id, station_name, station_abbr, station_latitude, station_longitude,bart_address in results]
    session.close()
    return jsonify(all_stations)


if __name__ == "__main__":
    app.run(debug=True)
