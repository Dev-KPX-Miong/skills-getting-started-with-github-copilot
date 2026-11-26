import pytest


def test_signup_adds_student_to_activity(client):
    # Arrange
    email = "new@mergington.edu"

    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Signed up new@mergington.edu for Chess Club"}
    participants = client.get("/activities").json()["Chess Club"]["participants"]
    assert email in participants


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    email = "new@mergington.edu"

    # Act
    response = client.post("/activities/Unknown Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_email_returns_400(client):
    # Arrange
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": existing_email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


@pytest.mark.xfail(strict=True, reason="max_participants is not enforced on signup yet")
def test_signup_rejects_when_activity_is_full(client):
    # Arrange: Basketball Team has max_participants=15 and no participants
    for i in range(15):
        client.post("/activities/Basketball Team/signup", params={"email": f"student{i}@mergington.edu"})

    # Act
    response = client.post("/activities/Basketball Team/signup", params={"email": "extra@mergington.edu"})

    # Assert
    assert response.status_code == 400
