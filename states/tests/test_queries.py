from unittest.mock import patch
import pytest

import states.queries as qry

def test_num_states():
    #current count of states in database
    old_count = qry.num_states()
    #adding a new state
    qry.create(qry.SAMPLE_STATE)
    #checking if a new state was created
    assert qry.num_states == old_count + 1