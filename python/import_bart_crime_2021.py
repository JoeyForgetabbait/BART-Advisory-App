# import dependencies
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
import pandas as pd

# create engine
engine = create_engine("postgresql://postgres:postgres@localhost:5432/bart_train_routes")

# declare base
Base = declarative_base()


class CrimeData(Base):
    __tablename__ = "bart_crime_report_2021"

    id = Column(Integer, primary_key=True)
    location = Column(String)
    date = Column(String)
    time = Column(String)
    charge_description = Column(String)


# Download the Excel file from the website
url = "https://www.bart.gov/sites/default/files/docs/2021%20UOF%20data%2020221007_redacted.xlsx"
response = requests.get(url)

# Load Excel data into a DataFrame
df = pd.read_excel(response.content)

# convert cit_charge to string
df["Cit: Charge"] = df["Cit: Charge"].astype(str)

# Remove bart and station from the location column
df["Inc: County/Location of occurrence"] = df["Inc: County/Location of occurrence"].str.replace(" BART", "")
df["Inc: County/Location of occurrence"] = df["Inc: County/Location of occurrence"].str.replace(" Station", "")

# Check if names are equal or one is a substring of the other


def clean_station_name(new_crime_data):
    if "North Concord" in new_crime_data:
        return "North Concord/Martinez"
    elif "24th Street" in new_crime_data:
        return "24th St. Mission"
    elif "Antioch E-Bart" in new_crime_data:
        return "Antioch"
    elif "West Dublin" in new_crime_data:
        return "West Dublin/Pleasanton"
    elif "Civic Center" in new_crime_data:
        return "Civic Center/UN Plaza"
    elif "16th Street" in new_crime_data:
        return "16th St. Mission"
    elif "El Cerrito Del Nort" in new_crime_data:
        return "El Cerrito del Norte"
    elif "Berryessa/N San Jose" in new_crime_data:
        return "Berryessa/North San Jose"
    elif "SFO" in new_crime_data:
        return "San Francisco International Airport"
    elif "Powell" in new_crime_data:
        return "Powell St."
    elif "Pleasant Hill" in new_crime_data:
        return "Pleasant Hill/Contra Costa Centre"
    elif "12th Street" in new_crime_data:
        return "12th St. Oakland City Center"
    elif "Montgomery" in new_crime_data:
        return "Montgomery St."
    else:
        return new_crime_data


df["Inc: County/Location of occurrence"] = df["Inc: County/Location of occurrence"].apply(clean_station_name)

# Remove instances San Francisco County,  San Mateo County, Oakland Shops, Pittsburg, Oakland West, Berkeley
df = df[~df["Inc: County/Location of occurrence"].isin(["San Francisco County", "San Mateo County", "Oakland Shops", "Pittsburg", "Oakland West", "Berkeley", "Not on Property"])]

# create table
Base.metadata.create_all(engine)

# create session
Session = sessionmaker(bind=engine)
session = Session()

# Iterate over DataFrame rows and insert data into the database
for index, row in df.iterrows():
    bart_crime_report_2021 = CrimeData(location=row["Inc: County/Location of occurrence"], date=row["Inc: Occurred date"], time=row["Inc: Occurred time"], charge_description=row["Cit: Charge"])
    session.add(bart_crime_report_2021)

# Commit the transaction
session.commit()

# Close the session
session.close()
