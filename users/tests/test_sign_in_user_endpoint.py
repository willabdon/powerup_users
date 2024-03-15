import json
import jwt
import pytest

from datetime import datetime, timedelta

from django.conf import settings

from users.tests.factories import USER_TEST_PASSWORD


URL = "/api/token/"


@pytest.fixture
def sign_in_request_data(user):
    return {
        "email": user.email,
        "password": USER_TEST_PASSWORD,
    }


@pytest.mark.django_db
def test_success_request(api_client, sign_in_request_data, user):
    response = api_client.post(
        URL.format(id=user.id),
        data=json.dumps(sign_in_request_data),
        content_type="application/json",
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_access_and_refresh_token_on_response(api_client, sign_in_request_data):
    response = api_client.post(
        URL, data=json.dumps(sign_in_request_data), content_type="application/json"
    )
    data = response.json()
    assert "access" in data
    assert "refresh" in data


@pytest.mark.django_db
@pytest.mark.test
def test_expire_time_is_24_h(api_client, sign_in_request_data):
    response = api_client.post(
        URL, data=json.dumps(sign_in_request_data), content_type="application/json"
    )
    data = response.json()
    access_token = data["access"]
    payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
    exp = datetime.fromtimestamp(payload["exp"]).strftime("%Y-%m-%d %H:%M:%S")
    future_time = (datetime.now() + timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")
    assert exp == future_time


@pytest.mark.django_db
def test_expire_time_is_6_months_if_rembember_me_is_true(
    api_client, sign_in_request_data
):
    sign_in_request_data["remember_me"] = True
    response = api_client.post(
        URL, data=json.dumps(sign_in_request_data), content_type="application/json"
    )
    data = response.json()
    access_token = data["access"]
    payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
    exp = datetime.fromtimestamp(payload["exp"]).strftime("%Y-%m-%d %H:%M:%S")
    future_time = (datetime.now() + timedelta(weeks=26)).strftime("%Y-%m-%d %H:%M:%S")
    assert exp is not future_time
