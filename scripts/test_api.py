import pytest

from src.api.main import app


@pytest.fixture()
def client():
	app.config.update({"TESTING": True})
	with app.test_client() as test_client:
		yield test_client


def test_health_endpoint(client):
	response = client.get("/api/health")
	assert response.status_code == 200
	payload = response.get_json()
	assert payload["status"] == "ok"
	assert payload["service"] == "change-point-api"


def test_summary_endpoint(client):
	response = client.get("/api/summary")
	assert response.status_code == 200
	payload = response.get_json()
	assert "start_date" in payload
	assert "end_date" in payload
	assert payload["total_records"] > 0
	assert payload["event_count"] > 0


def test_prices_endpoint(client):
	response = client.get("/api/prices?start=2019-01-01&end=2019-01-31")
	assert response.status_code == 200
	payload = response.get_json()
	assert isinstance(payload, list)
	assert payload
	assert "date" in payload[0]
	assert "price" in payload[0]


def test_log_returns_endpoint(client):
	response = client.get("/api/log-returns?start=2019-01-01&end=2019-02-15")
	assert response.status_code == 200
	payload = response.get_json()
	assert isinstance(payload, list)
	assert payload
	assert "date" in payload[0]
	assert "log_return" in payload[0]


def test_events_endpoint(client):
	response = client.get("/api/events?start=2013-01-01&end=2022-12-31")
	assert response.status_code == 200
	payload = response.get_json()
	assert isinstance(payload, list)
	assert payload
	assert "date" in payload[0]
	assert "event_name" in payload[0]
	assert "category" in payload[0]


def test_change_point_endpoint(client):
	response = client.get("/api/change-point?window=30")
	assert response.status_code == 200
	payload = response.get_json()
	assert payload["window"] == 30
	assert payload["status"] in {"ok", "insufficient_data"}
	if payload["status"] == "ok":
		assert "change_point_date" in payload
		assert "mean_shift" in payload
