from fastapi.testclient import TestClient
from fastapi import status

app = __import__('app.03_restful_api.app', fromlist=['app'])

client = TestClient(app.app)

def test_return_health_check():
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'Healthy'}