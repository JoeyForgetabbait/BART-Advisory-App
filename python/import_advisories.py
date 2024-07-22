# import dependencies
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
from api_keys import bart_api_key
import pandas as pd

# create engine
engine = create_engine("postgresql://postgres:postgres@localhost:5432/bart_train_routes")

# declare base
Base = declarative_base()


class BartAdvisories(Base):
    __tablename__ = "bart_advisories"

    id = Column(Integer, primary_key=True)
    station = Column(String)
    description = Column(Text)
    sms_text = Column(Text)
    date = Column(String)
    time = Column(String)
    message = Column(String)


# Retrieve data from the BART API
response = requests.get("https://api.bart.gov/api/bsa.aspx", params={"cmd": "bsa", "key": bart_api_key, "json": "y"})
data = response.json()["root"]

# create table
Base.metadata.create_all(engine)

# create session
Session = sessionmaker(bind=engine)
session = Session()

# Extract relevant information
advisory_data = data["bsa"][0]
date = data["date"]
time = data["time"]
message = data["message"]

# Insert data into the database
record = BartAdvisories(station=advisory_data["station"], description=advisory_data["description"]["#cdata-section"], sms_text=advisory_data["sms_text"]["#cdata-section"], date=date, time=time, message=message)
session.add(record)

# Commit the transaction
session.commit()

# Close the session
session.close()
