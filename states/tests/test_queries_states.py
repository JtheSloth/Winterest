from unittest.mock import patch
import pytest

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import queries_states as qry

def test_num_states():
    old_count = qry.num_states() #current count of states in database
    qry.create(qry.SAMPLE_STATE) #adding a new state
    assert qry.num_states() == old_count + 1 #checking if a new state was created

    
def test_good_create():
    old_count = qry.num_states() #current count of states
    new_rec_id = qry.create(qry.SAMPLE_STATE) #new record
    assert qry.is_valid_id(new_rec_id) #checking if the new id created is a valid one
    assert qry.num_states() == old_count + 1 #sees if the new state was created

def test_create_bad_name():
    old_count = qry.num_states() #current count of states
    with pytest.raises(Exception):
        qry.create(None)
    assert qry.num_states() == old_count #ensuring no invalid state was created
    
def test_create_bad_param_type():
    old_count = qry.num_states() #current count of states
    with pytest.raises(Exception):
        qry.create([1, 2, 3])
    assert qry.num_states() == old_count #make sure number of states did not change


@patch('queries_states.db_connect')
def test_read(mock_db_connect):
    # create a test state
    new_rec_id = qry.create(qry.SAMPLE_STATE)

    # mock the MongoDB collection
    mock_collection = mock_db_connect.return_value.__getitem__.return_value
    mock_collection.find_one.return_value = {'id': new_rec_id, 'name': 'New York'}
    mock_collection.find.return_value = [{'id': '1', 'name': 'New York'}, {'id': '2', 'name': 'California'}]

    # test reading that specific state
    result = qry.read(new_rec_id)
    assert result is not None
    assert result['id'] == new_rec_id

    # test reading all states
    all_states = qry.read()
    assert isinstance(all_states, list)
    assert len(all_states) > 0
    
@patch('states.queries.db_connect', return_value=False, autospec=True)
def test_read_cant_connect(mock_db_connect):
    with pytest.raises(ConnectionError):
        states = qry.read()


def test_bad_test_for_num_states():
    # test that num_states returns a valid non-negative integer
    count = qry.num_states()
    assert isinstance(count, int) 
    assert count >= 0 

@patch('states.queries.db_connect', return_value=True, autospec=True)
def test_delete(mock_db_connect, temp_state):
    qry.delete(temp_state)
    assert temp_state not in qry.read()