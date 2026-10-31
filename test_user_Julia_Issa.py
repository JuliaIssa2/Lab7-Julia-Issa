"""Lab 7 tests for the existing SQLite functions and Flask API."""

import sqlite3

import pytest

import app as user_app


@pytest.fixture
def isolated_db(tmp_path, monkeypatch):
    """Send every application connection to a fresh database for this test."""
    database_path = tmp_path / "database.db"
    monkeypatch.setattr(
        user_app,
        "connect_to_db",
        lambda: sqlite3.connect(database_path),
    )
    return database_path


@pytest.fixture
def db(isolated_db):
    user_app.create_db_table()
    return isolated_db


@pytest.fixture
def user_data():
    return {
        "name": "Julia Issa",
        "email": "julia@example.com",
        "phone": "12345678",
        "address": "Beirut",
        "country": "Lebanon",
    }


@pytest.fixture
def saved_user(db, user_data):
    return user_app.insert_user(user_data)


@pytest.fixture
def client(db):
    return user_app.app.test_client()


def test_database_created_on_first_run(isolated_db):
    assert not isolated_db.exists()

    user_app.create_db_table()

    assert isolated_db.exists()
    with sqlite3.connect(isolated_db) as connection:
        columns = connection.execute("PRAGMA table_info(users)").fetchall()
    assert [column[1] for column in columns] == [
        "user_id", "name", "email", "phone", "address", "country"
    ]
    assert user_app.get_users() == [
        {
            "user_id": 1,
            "name": "Example",
            "email": "juliaissa@gmail.com",
            "phone": "769273909625",
            "address": "Beirut",
            "country": "Lebanon",
        },
        {
            "user_id": 2,
            "name": "Nour",
            "email": "Nour@gmail.com",
            "phone": "769273909625",
            "address": "Beirut",
            "country": "Lebanon",
        },
    ]


def test_existing_database_is_not_reseeded(db):
    original_users = user_app.get_users()
    user_app.delete_user(original_users[0]["user_id"])

    user_app.create_db_table()

    assert user_app.get_users() == original_users[1:]


def test_insert_user(db, user_data):
    inserted = user_app.insert_user(user_data)

    assert isinstance(inserted["user_id"], int)
    assert inserted["user_id"] > 0
    assert inserted == {"user_id": inserted["user_id"], **user_data}
    assert user_app.get_user_by_id(inserted["user_id"]) == inserted


def test_get_users(db, user_data):
    initial_users = user_app.get_users()
    first = user_app.insert_user(user_data)
    second = user_app.insert_user({**user_data, "name": "Nour Issa"})

    assert sorted(user_app.get_users(), key=lambda user: user["user_id"]) == [
        *initial_users, first, second
    ]


def test_get_user_by_id(saved_user):
    assert user_app.get_user_by_id(saved_user["user_id"]) == saved_user


def test_update_user(saved_user):
    changed = {**saved_user, "name": "Julia Updated", "email": "new@example.com"}

    assert user_app.update_user(changed) == changed
    assert user_app.get_user_by_id(saved_user["user_id"]) == changed


def test_delete_user(saved_user):
    assert user_app.delete_user(saved_user["user_id"]) == {
        "status": "User deleted successfully"
    }
    assert user_app.get_user_by_id(saved_user["user_id"]) == {}


def test_api_get_users(client, user_data):
    initial_users = user_app.get_users()
    first = user_app.insert_user(user_data)
    second = user_app.insert_user({**user_data, "name": "Nour Issa"})

    response = client.get("/api/users")

    assert response.status_code == 200
    assert sorted(response.get_json(), key=lambda user: user["user_id"]) == [
        *initial_users, first, second
    ]


def test_api_get_user(client, user_data):
    saved = user_app.insert_user(user_data)

    response = client.get(f"/api/users/{saved['user_id']}")

    assert response.status_code == 200
    assert response.get_json() == saved


def test_api_add_user(client, user_data):
    response = client.post("/api/users/add", json=user_data)

    assert response.status_code == 200
    uploaded = response.get_json()
    assert uploaded == {"user_id": uploaded["user_id"], **user_data}
    assert user_app.get_user_by_id(uploaded["user_id"]) == uploaded


def test_api_update_user(client, user_data):
    saved = user_app.insert_user(user_data)
    changed = {**saved, "name": "Julia Updated", "email": "new@example.com"}

    response = client.put("/api/users/update", json=changed)

    assert response.status_code == 200
    assert response.get_json() == changed
    assert user_app.get_user_by_id(saved["user_id"]) == changed


def test_api_delete_user(client, user_data):
    saved = user_app.insert_user(user_data)

    response = client.delete(f"/api/users/delete/{saved['user_id']}")

    assert response.status_code == 200
    assert response.get_json() == {"status": "User deleted successfully"}
    assert user_app.get_user_by_id(saved["user_id"]) == {}
