import pytest


def test_root_redirects_to_static_index(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_get_activities_returns_data(client):
    # Arrange

    # Act
    response = client.get("/activities")
    json_data = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(json_data, dict)
    assert "Chess Club" in json_data
    assert "participants" in json_data["Chess Club"]


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    json_data = response.json()

    # Assert
    assert response.status_code == 200
    assert json_data["message"] == f"Signed up {email} for {activity_name}"
    assert email in client.get("/activities").json()[activity_name]["participants"]


def test_duplicate_signup_returns_bad_request(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    json_data = response.json()

    # Assert
    assert response.status_code == 400
    assert json_data["detail"] == "Student already signed up"
    participants = client.get("/activities").json()[activity_name]["participants"]
    assert participants.count(email) == 1


def test_remove_participant_deletes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")
    json_data = response.json()

    # Assert
    assert response.status_code == 200
    assert json_data["message"] == f"Removed {email} from {activity_name}"
    assert email not in client.get("/activities").json()[activity_name]["participants"]
