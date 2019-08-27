import pytest
from tld import exceptions
from utils import get_authoritative_nameserver


def test_ok():
    assert type(get_authoritative_nameserver("jolvera.dev")) is list
    assert type(get_authoritative_nameserver("https://jolvera.dev")) is list


def test_wrong_tld():
    with pytest.raises(exceptions.TldDomainNotFound):
        get_authoritative_nameserver("jolvera.abcdefghi")

    with pytest.raises(exceptions.TldDomainNotFound):
        get_authoritative_nameserver("https://jolvera.abcdefghi")


def test_no_tld():
    with pytest.raises(exceptions.TldDomainNotFound):
        get_authoritative_nameserver("jolvera")

    with pytest.raises(exceptions.TldDomainNotFound):
        get_authoritative_nameserver("https://jolveral")


def test_wrong_schema():
    with pytest.raises(exceptions.TldBadUrl):
        get_authoritative_nameserver("https:////jolvera.dev")


def test_no_domain():
    with pytest.raises(TypeError):
        get_authoritative_nameserver()
