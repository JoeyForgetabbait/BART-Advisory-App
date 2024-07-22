# import dependencies
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
from api_keys import bart_api_key

# create engine
engine = create_engine("postgresql://postgres:postgres@localhost:5432/bart_train_routes")

# declare base
Base = declarative_base()


class BartRouteInfo(Base):
    __tablename__ = "bart_route_info"
    id = Column(Integer, primary_key=True)
    route_id = Column(String)
    name = Column(String)
    abbr = Column(String)
    origin = Column(String)
    destination = Column(String)
    direction = Column(String)
    hexcolor = Column(String)
    color = Column(String)
    num_stns = Column(Integer)
    config = Column(String)


#  retrieve data from api
response_route_info = requests.get("https://api.bart.gov/api/route.aspx", params={"cmd": "routeinfo", "route": "all", "key": bart_api_key, "json": "y"})
data_route_info = response_route_info.json()["root"]["routes"]["route"]

# create table
Base.metadata.create_all(engine)

# create session
Session = sessionmaker(bind=engine)
session = Session()

# Insert data into the database
for route in data_route_info:
    record = BartRouteInfo(route_id=route["routeID"], name=route["name"], abbr=route["abbr"], origin=route["origin"], destination=route["destination"], direction=route["direction"], hexcolor=route["hexcolor"], color=route["color"], num_stns=int(route["num_stns"]), config=route["config"]["station"])
    session.add(record)

# Commit the transaction
session.commit()

# Close the session
session.close()
