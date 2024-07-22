# Group 3, Project 6 README 

## Overview/Purpose
Our project focuses on BART (Bay Area Rapid Transit) station crime and train/station data. By organizing the data by station, for example where each crime report occured at, we found we could give riders or potential riders insight into the station they want to depart from or arrive to. The purpose of this is to inform the public of safety concerns, delays, and additional route information both in real time. 

## Instructions on Use and Interaction
- step 1: Create database in pgdmin 4
- step 2: Run the import scripts under the python folder (make sure database name, port, password, and username are correct for linking with pgadmin 4)
- step 3: Once all the data is correctly imported you are then able to run the app.py
- step 4: Once the app is running you are able to utilize the dropdown menu to check for crime at specific stations or check for current bar advisories
## Ethical Considerations
The main ethical consideration in our project pertains to personally identifiable information (PII). Our crime report data set includes race, gender, and birth date, which can cause in andividual's identity to be found or information used without their permission. This information should be removed or anonymized, and access to the data set should be controlled and/or limited. The purpose of using this data set is not to be able to identify certain individuals, but to provide general safety alerts/knowledge to the public riding BART.

Additionally, our project uses BART police and transportation data for educational purposes only. If we wanted to actually create this application outside of the classroom, it would be neccesary to at least get copyright permissions for data sources, API documentation, and BART logos etc. 

## References (Data)
- https://www.bart.gov/sites/default/files/docs/2021%20UOF%20data%2020221007_redacted.xlsx
- https://api.bart.gov/docs/overview/index.aspx

## References (Additional Code/Help with Code, etc)
- Class Lecture/Exercises
- Chat GPT
- GeeksForGeeks.org
- https://www.wrm.org/media/k2/items/cache/e2acd849d365015ef08ef5b696dc9e31_XL.jpg (App front page image)
