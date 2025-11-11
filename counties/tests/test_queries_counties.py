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


@patch('queries_counties.db_connect', return_value=False, autospec=True)
def test_read_cant_connect(mock_db_connect):
    with pytest.raises(ConnectionError):
        counties = qry.read()
