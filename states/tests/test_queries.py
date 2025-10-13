from unittest.mock import patch
import pytest

import queries as qry

def test_num_states():
    old_count = qry.num_states() #current count of states in database
    qry.create(qry.SAMPLE_STATE) #adding a new state
    assert qry.num_states == old_count + 1 #checking if a new state was created

    
def test_good_create():
    old_count = qry.num_states() #current count of states
    new_rec_id = qry.create(qry.SAMPLE_STATE) #new record 
    assert qry.is_valid_id(new_rec_id) #checking if the new id created is a valid one
    assert qry.num_states == old_count + 1 #sees if the new state was created
    
