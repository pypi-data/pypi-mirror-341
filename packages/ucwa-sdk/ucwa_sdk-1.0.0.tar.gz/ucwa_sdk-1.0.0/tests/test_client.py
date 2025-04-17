import pytest
from ucwa_sdk.client import UCWAClient

def test_create_client():
    client = UCWAClient(api_key="your-api-key")
    assert client is not None
