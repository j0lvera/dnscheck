import pytest
import json
from webtest import TestApp
from index import app


def test_root_redirect():
    webapp = TestApp(app)
    response = webapp.get("/")

    assert response.status_code == 302
    assert response.location == "https://dnscheck.now.sh"

    webapp.reset()


def test_ok():
    webapp = TestApp(app)
    response = webapp.post("/", dict(domain="jolvera.dev", dns_server="1.1.1.1"))

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert "data" in json.loads(response.body)

    webapp.reset()
