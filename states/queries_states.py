from pymongo import MongoClient

MIN_ID_LEN = 1
ID = 'id'
NAME = 'name'
POPULATION = 'population'
CAPITAL = 'capital'
GOVERNOR = 'governor'

SAMPLE_STATE = {
    NAME: 'New York',
    POPULATION: 19870000,
    CAPITAL: 'Albany',
    GOVERNOR: 'Kathy Hochul'
}

state_cache = {
    "1": SAMPLE_STATE,
}

read_cache = {}


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


def is_valid_governor(_governor: str):
    if not isinstance(_governor, str):
        return False
    if len(_governor) < MIN_ID_LEN:
        return False
    return True


def num_states():
    return len(state_cache)


def create(fields: dict):
    if (not isinstance(fields, dict)):
        raise ValueError(f'Bad type for {type(fields)=}')
    if (not fields.get(NAME) or not isinstance(fields[NAME], str)):
        raise ValueError(f'Bad value for {fields.get(NAME)=}')
    if (not fields.get(CAPITAL) or not isinstance(fields[CAPITAL], str)):
        raise ValueError(f'Bad value for {fields.get(CAPITAL)=}')
    if (not fields.get(POPULATION) or not isinstance(fields[POPULATION], int)):
        raise ValueError(f'Bad value for {fields.get(POPULATION)=}')
    new_id = str(len(state_cache) + 1)
    state_cache[new_id] = fields
    return new_id


'''Connects to MongoDB database'''


def db_connect():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["statesdb"]
    return db


"""
Reads documents from the MongoDB
"""


def read(state_id=None):
    if state_id is not None:
        state_id = str(state_id)

        if state_id in read_cache:
            return read_cache[state_id]
        db = db_connect()
        if not db:
            raise ConnectionError("Failed to connect to database")
        collection = db["states"]

        doc = collection.find_one({ID: state_id}, {"_id": 0})
        read_cache[state_id] = doc
        return doc

    db = db_connect()
    if not db:
        raise ConnectionError("Failed to connect to database")
    collection = db["states"]
    return list(collection.find({}, {"_id": 0}))


def delete(state_id: str):
    if state_id not in state_cache:
        raise ValueError(f'No such state: {state_id}')
    del state_cache[state_id]
    return True