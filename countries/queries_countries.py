from pymongo import MongoClient

MIN_ID_LEN = 1
ID = 'id'
NAME = 'name'
POPULATION = 'population'
CONTENTIENT = 'contentient'
CAPITAL = 'capital'
GDP = 'gdp'
AREA = 'area'
FOUNDED = 'founded'
PRESIDENT = 'president'

SAMPLE_COUNTRY = {
    NAME: 'United States of America',
    POPULATION: 340000000,
    CONTENTIENT: 'North America',
    CAPITAL: 'Washington DC'
    GDP = '29.18 trillion USD'.
    AREA: '3,810,000 sq mi',
    FOUNDED: '1776',
    PRESIDENT: 'Donald Trump'
}


country_cache = {
    1: SAMPLE_COUNTRY
}


def is_valid_id(_id: str):
    if not isinstance(_id, str):
        return False
    if len(_id) < MIN_ID_LEN:
        return False
    return True

def is_valid_population(_population):
    if not isinstance(_population, int):
        return False
    if _population < 0:
        return False
    return True


def num_countries():
    return len(country_cache)


def create(fields: dict):
    if (not isinstance(fields, dict)):
        raise ValueError(f'Bad type for {type(fields)=}')
    if (not fields.get(NAME) or not isinstance(fields[NAME], str)):
        raise ValueError(f'Bad value for {fields.get(NAME)=}')
    if (not fields.get(POPULATION) or not isinstance(fields[POPULATION], int)):
        raise ValueError(f'Bad value for {fields.get(POPULATION)=}')
    if (not fields.get(CONTENTIENT) or not isinstance(fields[CONTENTIENT], str)):
        raise ValueError(f'Bad value for {fields.get(CONTENTIENT)=}')
    if (not fields.get(CAPITAL) or not isinstance(fields[CAPITAL], str)):
        raise ValueError(f'Bad value for {fields.get(CAPITAL)=}')
    if (not fields.get(GDP) or not isinstance(fields[GDP], str)):
        raise ValueError(f'Bad value for {fields.get(GDP)=}')
    if (not fields.get(AREA) or not isinstance(fields[AREA], str)):
        raise ValueError(f'Bad value for {fields.get(AREA)=}')
    if (not fields.get(FOUNDED) or not isinstance(fields[FOUNDED], str)):
        raise ValueError(f'Bad value for {fields.get(FOUNDED)=}')
    if (not fields.get(PRESIDENT) or not isinstance(fields[PRESIDENT], str)):
        raise ValueError(f'Bad value for {fields.get(PRESIDENT)=}')
    new_id = str(len(state_cache) + 1)
    state_cache[new_id] = fields
    return new_id


'''Connects to MongoDB database'''


def db_connect():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["countriesdb"]
    return db


"""
Reads documents from the MongoDB
"""


def read(country_id=None):
    db = db_connect()
    if not db:
        raise ConnectionError("Failed to connect to database")
    collection = db["countriesbd"]

    if country_id is None:
        # return all countries as a list
        return list(collection.find({}, {"_id": 0}))
    else:
        # find one country by its 'id'
        result = collection.find_one({"id": country_id}, {"_id": 0})
        return result


def delete(country_id: str):
    if country_id not in country_cache:
        raise ValueError(f'No such country: {country_id}')
    del state_cache[country_id]
    return True
