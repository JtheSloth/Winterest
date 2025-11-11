from pymongo import MongoClient

MIN_ID_LEN = 1
ID = 'id'
NAME = 'name'
POPULATION = 'population'
STATE = 'state'
AREA = 'area'
FOUNDED = 'founded'
COUNTY_SEAT = 'county_seat'

SAMPLE_COUNTY = {
    NAME: 'Los Angeles County',
    POPULATION: 10000000,
    STATE: 'California',
    AREA: '4,751 sq mi',
    FOUNDED: '1850',
    COUNTY_SEAT: 'Los Angeles'
}

county_cache = {
    1: SAMPLE_COUNTY,
}