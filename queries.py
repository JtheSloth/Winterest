from random import randint

MIN_ID_LEN = 1
ID = 'id'
NAME = 'name'

SAMPLE_STATE = {
    NAME: 'New York'
}

state_cache = {
    1: SAMPLE_STATE,
}

def is_valid_id(_id: str):
    if(not isinstance(_id, str)):
        return False
    if(len(_id) < MIN_ID_LEN):
        return False
    return True