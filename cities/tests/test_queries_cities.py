from unittest.mock import patch
import pytest
from contextlib import contextmanager

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import queries_cities as qry

@pytest.fixture(scope='function')
def temp_city():
    new_rec_id = qry.create(qry.SAMPLE_CITY)
    yield new_rec_id
    try:
        qry.delete(new_rec_id)
    except ValueError:
        print('The record was already deleted.')

#reset city_cache before every test
@pytest.fixture(autouse=True)
def reset_cache():
    cache = getattr(qry, "city_cache", None)
    if cache is not None:
        cache.clear()

@pytest.fixture
def city_delta():
    @contextmanager
    def _city_delta(delta=0):
        old_count = qry.num_cities()
        yield
        new_count = qry.num_cities()
        assert new_count - old_count == delta
    return _city_delta



def test_num_cities(city_delta):
    with city_delta(+1):  # expect +1 change
        qry.create(qry.SAMPLE_CITY)
    '''
    old_count = qry.num_cities() #current count of cities in database
    qry.create(qry.SAMPLE_CITY) #adding a new citie
    assert qry.num_cities() == old_count + 1 #checking if a new city was created'''

    
def test_good_create(city_delta):
    with city_delta(+1):  # expect +1 change
        new_rec_id = qry.create(qry.SAMPLE_CITY) #new record
        assert qry.is_valid_id(new_rec_id) #checking if the new id created is a valid one
    '''
    old_count = qry.num_cities() #current count of cities
    new_rec_id = qry.create(qry.SAMPLE_CITY) #new record
    assert qry.is_valid_id(new_rec_id) #checking if the new id created is a valid one
    assert qry.num_cities() == old_count + 1 #sees if the new citie was created'''
def test_create_bad_name(city_delta):
    with city_delta():
        with pytest.raises(Exception):
            qry.create(None)
    '''
    old_count = qry.num_cities() #current count of cities
    with pytest.raises(Exception):
        qry.create(None)
    assert qry.num_cities() == old_count #ensuring no invalid city was created'''
    
def test_create_bad_param_type(city_delta):
    with city_delta():
        with pytest.raises(Exception):
            qry.create([1, 2, 3])
    '''
    old_count = qry.num_cities() #current count of cities
    with pytest.raises(Exception):
        qry.create([1, 2, 3])
    assert qry.num_cities() == old_count #make sure number of cities did not change
    '''
@patch('queries_cities.db_connect')
def test_read(mock_db_connect, temp_city):

    # mock the MongoDB collection
    mock_collection = mock_db_connect.return_value.__getitem__.return_value
    mock_collection.find_one.return_value = {'id': temp_city, 'name': 'New York City'}
    mock_collection.find.return_value = [{'id': '1', 'name': 'New York City'}, {'id': '2', 'name': 'Los Angeles'}]

    # test reading that specific citie
    result = qry.read(temp_city)
    assert result is not None
    assert result['id'] == temp_city

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


def test_delete(temp_city,city_delta):
    
    assert temp_city in qry.city_cache
    with city_delta(-1): #expecting num_cities to decrease -1
        # delete the city
        qry.delete(temp_city)
    # verify it's no longer in the cache
    assert temp_city not in qry.city_cache 
