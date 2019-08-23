import pytest
from webtest import TestApp
from index import app


@pytest.mark.webtest
def test_index():
    webapp = TestApp(app)
    response = webapp.post("/", dict(domain="jolvera.dev"))

    print("response", response)

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

    webapp.reset()
