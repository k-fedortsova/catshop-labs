import requests


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.data == b"ok\n"


def test_ready(client):
    response = client.get("/ready")

    assert response.status_code == 200

    data = response.get_json()

    assert data["ready"] is True
    assert data["store"].startswith("file:")


def test_visits_counter_increments(client):
    first = client.get("/visits")
    second = client.get("/visits")

    assert first.status_code == 200
    assert second.status_code == 200

    assert first.get_json() == {
        "visits": 1,
        "store": "file",
    }

    assert second.get_json() == {
        "visits": 2,
        "store": "file",
    }


def test_price_with_stubbed_partner(client, monkeypatch):

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "sku": "MK-II",
                "price": "1234.56",
                "currency": "UAH",
            }

    requested = {}

    def fake_get(url, timeout):
        requested["url"] = url
        requested["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setattr(
        "app.requests.get",
        fake_get,
    )

    response = client.get("/price/MK-II")

    assert response.status_code == 200

    data = response.get_json()

    assert data["sku"] == "MK-II"
    assert data["price"] == "1234.56"
    assert data["currency"] == "UAH"

    assert requested["url"].endswith("/v1/catalog/MK-II")
    assert requested["timeout"] == 2.0


def test_price_partner_timeout_returns_502(client, monkeypatch):

    def fake_get(url, timeout):
        raise requests.Timeout("partner timed out")

    monkeypatch.setattr(
        "app.requests.get",
        fake_get,
    )

    response = client.get("/price/MK-II")

    assert response.status_code == 502

    data = response.get_json()

    assert data["sku"] == "MK-II"
    assert data["error"] == "Timeout"
    assert "partner timed out" in data["detail"]