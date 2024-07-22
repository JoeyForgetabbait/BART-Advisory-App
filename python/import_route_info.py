# import dependencies
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
from api_keys import bart_api_key

# create engine
engine = create_engine("postgresql://postgres:postgres@localhost:5432/bart_train_routes")

# declare base
Base = declarative_base()


# create model of table with info
class BartRoute(Base):
    __tablename__ = "bart_routes"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    abbr = Column(String)
    route_id = Column(String)
    number = Column(String)
    hexcolor = Column(String)
    color = Column(String)
    direction = Column(String)


# Retrieve data from the BART API
response = requests.get("https://api.bart.gov/api/route.aspx", params={"cmd": "routes", "key": bart_api_key, "json": "y"})
data = response.json()["root"]["routes"]["route"]

# create table
Base.metadata.create_all(engine)

# create session
Session = sessionmaker(bind=engine)
session = Session()

# Insert data into the database
for route in data:
    record = BartRoute(name=route["name"], abbr=route["abbr"], route_id=route["routeID"], number=route["number"], hexcolor=route["hexcolor"], color=route["color"], direction=route["direction"])
    session.add(record)


# Commit the transaction
session.commit()

# Close the session
session.close()
