from sqlalchemy import text


def test_login_success(client, db_session):
    db_session.execute(
        text("""
        INSERT INTO users (username, password_hash)
        VALUES ('john', '$2b$12$VbvbFKFa8ZkRCCuRVwi.uO4h7Rpcpdh8p38aGElB1QxhnFFeFMXMC')
    """)
    )
    db_session.commit()

    response = client.post(
        "/auth/login", data={"username": "john", "password": "s3cre7P@ssW0ra!"}
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_failure(client):
    response = client.post(
        "/auth/login", data={"username": "nosuchuser", "password": "wrong"}
    )
    assert response.status_code == 401
