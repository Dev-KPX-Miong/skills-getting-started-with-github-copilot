def test_unregister_removes_student_from_activity(client):
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.delete("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Unregistered michael@mergington.edu from Chess Club"}
    participants = client.get("/activities").json()["Chess Club"]["participants"]
    assert email not in participants


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.delete("/activities/Unknown Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_student_not_registered_returns_404(client):
    # Arrange
    email = "nobody@mergington.edu"

    # Act
    response = client.delete("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not registered for this activity"
