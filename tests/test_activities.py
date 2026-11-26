def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_count = 9

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == expected_count
    assert "Chess Club" in data


def test_each_activity_has_expected_fields(client):
    # Arrange
    expected_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    data = client.get("/activities").json()

    # Assert
    for name, activity in data.items():
        assert set(activity) == expected_fields, name
        assert isinstance(activity["participants"], list), name
        assert activity["max_participants"] > 0, name


def test_get_activities_includes_current_participants(client):
    # Arrange
    chess_participants = ["michael@mergington.edu", "daniel@mergington.edu"]

    # Act
    data = client.get("/activities").json()

    # Assert
    assert data["Chess Club"]["participants"] == chess_participants
    assert data["Basketball Team"]["participants"] == []
