## import dependencies
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
from api_keys import bart_api_key

# create engine
engine = create_engine("postgresql://postgres:postgres@localhost:5432/bart_train_routes")

# declare base
Base = declarative_base()


class BartStationInfo(Base):
    __tablename__ = "bart_station_info"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    abbr = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    address = Column(String)
    city = Column(String)
    county = Column(String)
    state = Column(String)
    zipcode = Column(String)


#  retrieve data from api
response_station_info = requests.get("https://api.bart.gov/api/stn.aspx", params={"cmd": "stns", "key": bart_api_key, "json": "y"})
data_station_info = response_station_info.json()["root"]["stations"]["station"]

# create table
Base.metadata.create_all(engine)

# create session
Session = sessionmaker(bind=engine)
session = Session()

# Insert data into the database
for station in data_station_info:
    record = BartStationInfo(name=station["name"], abbr=station["abbr"], latitude=station["gtfs_latitude"], longitude=station["gtfs_longitude"], address=station["address"], city=station["city"], county=station["county"], state=station["state"], zipcode=station["zipcode"])
    session.add(record)

# Commit the transaction
session.commit()

# Close the session
session.close()
