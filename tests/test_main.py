# tests/test_main.py

from fastapi.testclient import TestClient
from app.main import app

# FastAPI'nin TestClient'ını kullanarak app'imizi test ediyoruz
client = TestClient(app)


def test_health_check():
    """
    /healthz endpoint'inin 200 OK ve beklenen JSON'ı döndürdüğünü test eder.
    """
    response = client.get("/healthz")

    # 1. Durum kodunun 200 olduğunu doğrula
    assert response.status_code == 200

    # 2. Dönen JSON içeriğinin {"status": "OK"} olduğunu doğrula
    assert response.json() == {"status": "OK"}
