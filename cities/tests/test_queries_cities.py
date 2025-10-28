from unittest.mock import patch
import pytest

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import queries_cities as qry

@pytest.mark.ship
def test_num_cities():
    old_count = qry.num_cities() #current count of cities in database
    qry.create(qry.SAMPLE_CITY) #adding a new citie
    assert qry.num_cities() == old_count + 1 #checking if a new citie was created

@pytest.mark.skip
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

@pytest.mark.skip
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
    
@pytest.mark.skip
def test_delete(temp_city,city_delta):
    
    assert temp_city in qry.city_cache
    with city_delta(-1): #expecting num_cities to decrease -1
        # delete the city
        qry.delete(temp_city)
    # verify it's no longer in the cache
    assert temp_city not in qry.city_cache

def test_city_has_valid_state():
    city = qry.SAMPLE_CITY
    state = city.get(qry.STATE, "").strip()

    # Ensure 'state' field exists and has a non-empty string
    assert state, "City record should contain a non-empty 'state' value"
    assert isinstance(state, str), "'state' should be a string"
    
    invalid_values = {"unknown", "n/a", "none", "null", ""}
    assert state.lower() not in invalid_values, f"Invalid state value: {state}"

    valid_states = {
        "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut",
        "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
        "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
        "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
        "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina",
        "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island",
        "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
        "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
    }
    assert state in valid_states, f"'{state}' is not a recognized valid US state"

@pytest.fixture
def db_failure():
    with patch('queries_cities.db_connect') as mock_db_connect:
        mock_db = mock_db_connect.return_value
        mock_db.__getitem__.side_effect = Exception("Database failure")
        yield mock_db_connect

def test_read_handles_db_failure(db_failure):
    with pytest.raises(Exception) as exc_info:
        qry.read("123")
    assert "Database failure" in str(exc_info.value)


def test_city_has_valid_mayor():
    city = qry.SAMPLE_CITY
    mayor = city.get(qry.MAYOR, "")

    # Ensure 'state' field exists and has a non-empty string
    assert mayor, "City record should contain a non-rempty 'mayor' value"
    assert isinstance(mayor, str), "'mayor' should be a string"

    # Check that mayor name is not a placeholder or invalid value
    invalid_values = {"unknown", "n/a", "none", "null", "tbd", "vacant", ""}
    assert mayor.lower() not in invalid_values, f"Invalid mayor name: {mayor}"

    test_city = {
        qry.NAME: 'Test City',
        qry.POPULATION: '1,000',
        qry.STATE: 'Arkansas',
        qry.MAYOR: 'Richard'
    }

    test_mayor = test_city.get(qry.MAYOR)
    assert test_mayor == 'Richard', f"Expected mayor 'Richard, got '{test_mayor}'"
    assert isinstance(test_mayor, str), "Mayor name should be a string"
    assert len(test_mayor) > 0, "Mayor name should not be empty"