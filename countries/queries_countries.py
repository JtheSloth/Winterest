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