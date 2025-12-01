import data.db_connect as dbc

from functools import wraps

COUNTRIES_COLLECTION = "countries"

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
    CAPITAL: 'Washington DC',
    GDP: '29.18 trillion USD',
    AREA: '3,810,000 sq mi',
    FOUNDED: '1776',
    PRESIDENT: 'Donald Trump'
}


country_cache = None


def needs_cache(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        global country_cache
        if not country_cache:
            country_cache = {}
            docs = dbc.read(COUNTRIES_COLLECTION)
            for doc in docs:
                country_id = doc.get(ID)
                if country_id is not None:
                    country_cache[country_id] = doc
        return fn(*args, **kwargs)
    return wrapper


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


@needs_cache
def num_countries():
    return len(country_cache)


def create(fields: dict):
    if (not isinstance(fields, dict)):
        raise ValueError(f'Bad type for {type(fields)=}')
    if (not fields.get(NAME) or not isinstance(fields[NAME], str)):
        raise ValueError(f'Bad value for {fields.get(NAME)=}')
    if (not fields.get(POPULATION) or not isinstance(fields[POPULATION], int)):
        raise ValueError(f'Bad value for {fields.get(POPULATION)=}')
    if (not fields.get(CONTENTIENT) or not isinstance(fields[CONTENTIENT],
                                                      str)):
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
    new_id = dbc.create(COUNTRIES_COLLECTION, fields)
    country_cache[new_id] = fields
    return new_id


@needs_cache
def read(country_id=None):
    return dbc.read(COUNTRIES_COLLECTION)


def delete(name: str):
    result = dbc.delete(COUNTRIES_COLLECTION, {NAME: name})
    if result < 1:
        raise ValueError(f'Country not found: {name}')
    return result
