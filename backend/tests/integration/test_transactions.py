from sqlalchemy import text


def test_create_transaction(client, db_session, auth_token):
    auth_user_id = db_session.execute(
        text("""
        SELECT user_id FROM users WHERE username = 'testuser'
    """)
    ).scalar_one()

    # Sender contractor (belongs to auth user)
    sender_id = db_session.execute(
        text("""
        INSERT INTO contractors (user_id, name)
        VALUES (:uid, 'Sender')
        RETURNING contractor_id
    """),
        {"uid": auth_user_id},
    ).scalar_one()

    receiver_id = db_session.execute(
        text("""
        INSERT INTO contractors (user_id, name)
        VALUES (:uid, 'Receiver')
        RETURNING contractor_id
    """),
        {"uid": auth_user_id},
    ).scalar_one()

    status_id = db_session.execute(
        text("""
        INSERT INTO transaction_statuses (code)
        VALUES ('OK')
        RETURNING status_id
    """)
    ).scalar_one()

    type_id = db_session.execute(
        text("""
        INSERT INTO transaction_types (code)
        VALUES ('PAYMENT')
        RETURNING transaction_type_id
    """)
    ).scalar_one()

    response = client.post(
        "/transactions/create",
        json={
            "contractor_from_id": sender_id,
            "contractor_to_id": receiver_id,
            "amount": "50.00",
            "status_id": status_id,
            "transaction_type_id": type_id,
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["contractor_to"] == "Receiver"
    assert body["amount"] == "50.00"


def test_create_transaction_unauthorized(client):
    response = client.post(
        "/transactions/create",
        json={
            "contractor_from_id": 1,
            "contractor_to_id": 2,
            "amount": "10",
            "status_id": 1,
            "transaction_type_id": 1,
        },
    )
    assert response.status_code == 401
