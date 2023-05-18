import uuid

import pytest
from fastapi.testclient import TestClient
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)
from unittest.mock import Mock, AsyncMock

from api.app.models import UserModel
from main import app

client = TestClient(app)

user_id = uuid.uuid4()
access_token = uuid.uuid4()

mock_users = Mock()
mock_users.create_user = AsyncMock()
mock_users.create_user.return_value = UserModel(id_=user_id, username="feric", access_token=access_token)


async def mock_get_users_list():
    return [
        UserModel(id_=uuid.uuid4(), username="user1", access_token=uuid.uuid4()),
        UserModel(id_=uuid.uuid4(), username="user2", access_token=uuid.uuid4()),
        UserModel(id_=uuid.uuid4(), username="user3", access_token=uuid.uuid4())
    ]

mock_users.get_users_list = mock_get_users_list

app.state.users = mock_users


class TestUserView:

    @pytest.mark.asyncio
    async def test_create_user_without_name(self):
        response = client.post("/api/user/", json={"username": ""})
        assert response.status_code == HTTP_400_BAD_REQUEST

    @pytest.mark.asyncio
    async def test_create_user(self):
        response = client.post("/api/user/", json={"username": "feric"})

        assert response.status_code == HTTP_200_OK

        data = response.json()
        assert "access_token" in data
        assert "user_id" in data

        assert data["access_token"] == str(access_token)
        assert data["user_id"] == str(user_id)

    @pytest.mark.asyncio
    async def test_get_users_non_empty_list(self):
        response = client.get("/api/users/")
        assert response.status_code == HTTP_200_OK
        assert response.json() == ["user1", "user2", "user3"]


class TestRecordView:
    def test_add_record(self):
        response = client.post(
            "/api/record/",
            json={"user_in": {"user_id": str(user_id), "access_token": str(access_token),}},
            files={"file": ("test.wav", open("test.wav", "rb"))},
        )
        print(response.content)
        assert response.status_code == HTTP_200_OK
        assert "record_url" in response.json()


    def test_add_record_invalid_token(mock_user_dependency, mock_app_dependency):
        response = client.post(
            "/records/",
            files={"file": ("test.wav", open("test.wav", "rb"))},
            data={"access_token": "invalid_token"}
        )
        assert response.status_code == HTTP_403_FORBIDDEN
        assert response.json()["detail"] == "Access token established or wrong"


    def test_add_record_no_user(mock_app_dependency):
        response = client.post(
            "/records/",
            files={"file": ("test.wav", open("test.wav", "rb"))},
            data={"access_token": "test_token"}
        )
        assert response.status_code == HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "User not found"


    def test_teapot():
        response = client.get("/api_v1/teapot/")
        assert response.status_code == HTTP_418_IM_A_TEAPOT
        assert response.json()["detail"] == "I'm a Teapot"


    def test_get_record(mock_user_dependency, mock_app_dependency):
        response = client.get("/record?record_id=test_id")
        assert response.status_code == HTTP_200_OK


    def test_get_record_no_user(mock_app_dependency):
        response = client.get("/record?record_id=test_id")
        assert response.status_code == HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "User not found"


    def test_get_record_not_found(mock_user_dependency, mock_app_dependency):
        response = client.get("/record?record_id=invalid_id")
        assert response.status_code == HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Record not found"


    def test_get_record_list_by_user(mock_user_dependency, mock_app_dependency):
        response = client.get("/record/list?access_token=test_token")
        assert response.status_code == HTTP_200_OK
        assert "test_record" in response.json()
        assert response.json()["test_record"] == "http://test-host/records/1/test_id"