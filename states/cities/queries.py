from pymongo import MongoClient

MIN_ID_LEN = 1
ID = 'id'
NAME = 'name'
POPULATION = 'population'
STATE = 'state'
AREA = 'area'
FOUNDED = 'founded'
MAYOR = 'mayor'

SAMPLE_CITY = {
    NAME: 'New York City',
    POPULATION: '8,478,000',
    STATE: 'New York',
    AREA: '469 sq mi',
    FOUNDED: '1624',
    MAYOR: 'Eric Adams'
}


city_cache = {
    1: SAMPLE_CITY
}


def is_valid_id(_id: str):
    if not isinstance(_id, str):
        return False
    if len(_id) < MIN_ID_LEN:
        return False
    return True


def num_cities():
    return len(city_cache)


def create(fields: dict):
    if (not isinstance(fields, dict)):
        raise ValueError(f'Bad type for {type(fields)=}')
    if (not fields.get(NAME)):
        raise ValueError(f'Bad value for {fields.get(NAME)=}')
    new_id = str(len(city_cache) + 1)
    city_cache[new_id] = fields
    return new_id


    '''Connects to MongoDB database'''


def db_connect():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["citiedb"]
    return db
    
    
"""
Reads documents from the MongoDB
"""

def read(city_id=None):
    db = db_connect
    collection = db["cities"]
    
    if city_id is None:
        # return all cities as a list
        return list(collection.find({}, {"_id": 0}))
    else:
        # find one city by its 'id'
        result = collection.find_one({"id": city_id}, {"_id": 0})
        return result
        
def delete(city_id: str):
    if city_id not in city_cache:
        raise ValueError(f'No such city: {city_id}')
    del city_cache[city_id]
    return True
