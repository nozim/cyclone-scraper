# Cyclones data scraping for https://rammb-data.cira.colostate.edu/tc_realtime/ 

## Description of project folders 

 - tasks - contains all the celery related functionality, schedule and taskts
 - scraper - has all the logic for extracting data from target resource
 - repo - is repository for saving data into db
 - api - REST api 
 
## Prerequisites 
 * Docker 19.03.8+
 * docker-compose 1.26.0
 * Python 3.8.2
