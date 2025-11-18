from copy import deepcopy
from unittest.mock import patch
import pytest

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import queries_counties as qry

def create_temp_county():
    return deepcopy(qry.SAMPLE_COUNTY)

@pytest.fixture(scope='function')
def temp_county():
    temp_county = create_temp_county()
    new_id = qry.create(create_temp_county())
    yield new_id
    try:
        qry.delete(new_id)
    except ValueError:
        print('The record has already been deleted.')


def test_create_bad_name():
    old_count = qry.num_counties() #current count of counties
    with pytest.raises(Exception):
        qry.create(None)
    assert qry.num_counties() == old_count #ensuring no invalid county was created

def test_create_bad_param_type():
    old_count = qry.num_counties() #current count of counties
    with pytest.raises(Exception):
        qry.create([1, 2, 3])
    assert qry.num_counties() == old_count #make sure number of counties did not change
    
@patch('queries_counties.db_connect')
def test_read(mock_db_connect, temp_county):
    # create a test county
    # new_rec_id = qry.create(qry.SAMPLE_COUNTY)

    # mock the MongoDB collection
    mock_collection = mock_db_connect.return_value.__getitem__.return_value
    mock_collection.find_one.return_value = {'id': temp_county, 'name': 'Queens'}
    mock_collection.find.return_value = [{'id': '1', 'name': 'Queens'}, {'id': '2', 'name': 'Bronx'}]

    # test reading that specific county
    result = qry.read(temp_county)
    assert result is not None
    assert result['id'] == temp_county

    # test reading all counties
    all_counties = qry.read()
    assert isinstance(all_counties, list)
    assert len(all_counties) > 0


@patch('queries_counties.db_connect', return_value=False, autospec=True)
def test_read_cant_connect(mock_db_connect):
    with pytest.raises(ConnectionError):
        counties = qry.read()


@pytest.mark.skip
def test_good_create(temp_county):
    assert qry.is_valid_id(temp_county) # checking if the id is valid
    assert temp_county in qry.county_cache # verify the county was created


def test_create_bad_population():
    old_count = qry.num_counties() #current count of counties
    with pytest.raises(Exception):
        qry.create({'name': 'Test County', 'population': 'not a number', 'state': 'California', 'area': '100 sq mi', 'founded': '1900', 'county_seat': 'Test City'})
    assert qry.num_counties() == old_count #ensuring no invalid county was created
