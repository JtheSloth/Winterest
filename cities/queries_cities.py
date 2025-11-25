import data.db_connect as dbc
COLLECTION = 'cities'

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
    new_id = dbc.create(COLLECTION, fields)
    city_cache[new_id] = fields
    return new_id


def read(city_id=None):
    return dbc.read(COLLECTION)


def delete(city_id: str):
    result = dbc.delete(COLLECTION, {ID: city_id})
    if result < 1:
        raise ValueError(f'City not found: {city_id}')
    return result
