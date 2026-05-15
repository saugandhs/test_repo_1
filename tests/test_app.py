def test_get_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200

    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_success(client):
    email = "test.student@mergington.edu"
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}

    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]


def test_duplicate_signup_returns_400(client):
    email = "duplicate@student.com"
    client.post("/activities/Chess%20Club/signup", params={"email": email})

    response = client.post("/activities/Chess%20Club/signup", params={"email": email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"


def test_signup_missing_activity_returns_404(client):
    response = client.post(
        "/activities/Nonexistent%20Club/signup",
        params={"email": "user@example.com"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant_success(client):
    email = "michael@mergington.edu"
    response = client.delete(
        "/activities/Chess%20Club/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from Chess Club"}

    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]


def test_remove_nonexistent_participant_returns_404(client):
    response = client.delete(
        "/activities/Chess%20Club/signup",
        params={"email": "missing@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
