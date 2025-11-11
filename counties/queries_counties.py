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


def is_valid_id(_id: str):
    if not isinstance(_id, str):
        return False
    if len(_id) < MIN_ID_LEN:
        return False
    return True


def num_counties():
    return len(county_cache)


def is_valid_population(_population):
    if not isinstance(_population, int):
        return False
    if _population < 0:
        return False
    return True


def create(fields: dict):

    if not isinstance(fields, dict):
        raise ValueError(f'Bad type for {type(fields)=}')

    if not fields.get(NAME) or not isinstance(fields[NAME], str):
        raise ValueError(f'Bad value for {fields.get(NAME)=}')

    if not fields.get(POPULATION) or not isinstance(fields[POPULATION], int):
        raise ValueError(f'Bad value for {fields.get(POPULATION)=}')

    if not fields.get(STATE) or not isinstance(fields[STATE], str):
        raise ValueError(f'Bad value for {fields.get(STATE)=}')

    if not fields.get(AREA) or not isinstance(fields[AREA], str):
        raise ValueError(f'Bad value for {fields.get(AREA)=}')

    if not fields.get(FOUNDED) or not isinstance(fields[FOUNDED], str):
        raise ValueError(f'Bad value for {fields.get(FOUNDED)=}')

    if not fields.get(COUNTY_SEAT) or not isinstance(fields[COUNTY_SEAT], str):
        raise ValueError(f'Bad value for {fields.get(COUNTY_SEAT)=}')

    new_id = str(len(county_cache) + 1)
    county_cache[new_id] = fields
    return new_id


'''Connects to MongoDB database'''


def db_connect():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["countydb"]
    return db


"""
Reads documents from the MongoDB
"""


def read(county_id=None):
    db = db_connect()
    if not db:
        raise ConnectionError("Failed to connect to database")
    collection = db["counties"]

    if county_id is None:
        # return all counties as a list
        return list(collection.find({}, {"_id": 0}))
    else:
        # find one county by its 'id'
        result = collection.find_one({"id": county_id}, {"_id": 0})
        return result


def delete(county_id: str):
    if county_id not in county_cache:
        raise ValueError(f'No such county: {county_id}')
    del county_cache[county_id]
    return True
