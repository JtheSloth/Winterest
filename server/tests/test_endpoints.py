from http.client import (
    BAD_REQUEST,
    FORBIDDEN,
    NOT_ACCEPTABLE,
    NOT_FOUND,
    OK,
    SERVICE_UNAVAILABLE,
)

from unittest.mock import patch

import pytest

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import endpoints as ep

TEST_CLIENT = ep.app.test_client()


def test_hello():
    resp = TEST_CLIENT.get(ep.HELLO_EP)
    resp_json = resp.get_json()
    assert ep.HELLO_RESP in resp_json

def test_echo_roundtrip_no_patch():
    payload = {"msg": "hi", "n": 7}
    resp = TEST_CLIENT.post("/echo", json=payload)
    assert resp.status_code == OK
    assert resp.get_json() == {"echo": payload}
    
@patch("endpoints.request.get_json")
def test_echo_uses_request_get_json_once(mock_get_json):
    # First patch test. forcing specific return value
    mock_get_json.return_value = {"foo": "bar"}
    resp = TEST_CLIENT.post("/echo", json={})
    assert resp.status_code == OK
    assert resp.get_json() == {"echo": {"foo": "bar"}}
    mock_get_json.assert_called_once_with(force=True)
    
@patch("endpoints.request.get_json", return_value=None)
def test_echo_handles_none_payload(mock_get_json):
    # Second patch test for invalid JSON
    resp = TEST_CLIENT.post("/echo", json={})
    assert resp.status_code == OK
    assert resp.get_json() == {"echo": None}
    mock_get_json.assert_called_once_with(force=True)
