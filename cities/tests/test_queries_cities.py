from unittest.mock import patch
import pytest

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import queries_cities as qry

def test_num_cities():
    old_count = qry.num_cities() #current count of cities in database
    qry.create(qry.SAMPLE_CITY) #adding a new citie
    assert qry.num_cities() == old_count + 1 #checking if a new citie was created

    
def test_good_create():
    old_count = qry.num_cities() #current count of cities
    new_rec_id = qry.create(qry.SAMPLE_CITY) #new record
    assert qry.is_valid_id(new_rec_id) #checking if the new id created is a valid one
    assert qry.num_cities() == old_count + 1 #sees if the new citie was created

def test_create_bad_name():
    old_count = qry.num_cities() #current count of cities
    with pytest.raises(Exception):
        qry.create(None)
    assert qry.num_cities() == old_count #ensuring no invalid citie was created
    
def test_create_bad_param_type():
    old_count = qry.num_cities() #current count of cities
    with pytest.raises(Exception):
        qry.create([1, 2, 3])
    assert qry.num_cities() == old_count #make sure number of cities did not change


@patch('queries_cities.db_connect')
def test_read(mock_db_connect):
    # create a test city
    new_rec_id = qry.create(qry.SAMPLE_CITY)

    # mock the MongoDB collection
    mock_collection = mock_db_connect.return_value.__getitem__.return_value
    mock_collection.find_one.return_value = {'id': new_rec_id, 'name': 'New York City'}
    mock_collection.find.return_value = [{'id': '1', 'name': 'New York City'}, {'id': '2', 'name': 'Los Angeles'}]

    # test reading that specific citie
    result = qry.read(new_rec_id)
    assert result is not None
    assert result['id'] == new_rec_id

    # test reading all cities
    all_cities = qry.read()
    assert isinstance(all_cities, list)
    assert len(all_cities) > 0


@patch('queries_cities.db_connect', return_value=False, autospec=True)
def test_read_cant_connect(mock_db_connect):
    with pytest.raises(ConnectionError):
        cities = qry.read()


def test_bad_test_for_num_cities():
    # test that num_cities returns a valid non-negative integer
    count = qry.num_cities()
    assert isinstance(count, int)
    assert count >= 0


def test_delete():
    # create a test city to delete
    new_rec_id = qry.create(qry.SAMPLE_CITY)
    assert new_rec_id in qry.city_cache
    # delete the city
    qry.delete(new_rec_id)
    # verify it's no longer in the cache
    assert new_rec_id not in qry.city_cache 
