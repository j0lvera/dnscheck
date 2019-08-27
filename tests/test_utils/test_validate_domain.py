import pytest
from tld import exceptions
from utils import validate_domain


def test_ok():
    assert validate_domain("jolvera.dev") == "jolvera.dev"
    assert validate_domain("https://jolvera.dev") == "jolvera.dev"
