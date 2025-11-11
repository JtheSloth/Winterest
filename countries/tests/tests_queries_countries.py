from copy import deepcopy
from unittest.mock import patch
import pytest

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import queries_countries as qry


def create_temp_country():
    return deepcopy(qry.SAMPLE_COUNTRY)


@pytest.fixture(scope='function')
def temp_country():
    new_id = qry.create(create_temp_country())
    yield new_id
    try:
        qry.delete(new_id)
    except ValueError:
        print('The record has already been deleted.')


def test_create_bad_name():
    old_count = qry.num_countries()  # current count of countries
    with pytest.raises(Exception):
        qry.create(None)
    # ensuring no invalid country was created
    assert qry.num_countries() == old_count