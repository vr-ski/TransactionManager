from sqlalchemy import text


def test_list_contractors_for_user(client, db_session, test_user, auth_token):
    # Insert contractors for the test user
    db_session.execute(
        text(
            """
            INSERT INTO contractors (user_id, name)
            VALUES (:uid, 'Alice'), (:uid, 'Bob')
            """
        ),
        {"uid": test_user["user_id"]},
    )
    db_session.commit()

    response = client.get(
        f"/contractors/user/{test_user['user_id']}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    names = [c["name"] for c in data]
    assert "Alice" in names
    assert "Bob" in names
