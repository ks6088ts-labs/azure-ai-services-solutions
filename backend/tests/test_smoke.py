from backend.tests.utilities import client


def test_main():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["openapi"] == "3.0.0"
