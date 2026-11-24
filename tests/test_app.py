from app.app import app


def client():
    return app.test_client()


def test_index():
    r = client().get("/")
    assert r.status_code == 200
    assert "WorkforceHub" in r.get_json()["message"]


def test_health():
    r = client().get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_list_employees():
    r = client().get("/api/employees")
    assert r.status_code == 200
    assert len(r.get_json()) >= 2


def test_add_employee():
    r = client().post("/api/employees", json={"name": "Meena", "role": "QA"})
    assert r.status_code == 201


def test_add_employee_invalid():
    r = client().post("/api/employees", json={"name": "NoRole"})
    assert r.status_code == 400