from api_tests.data.auth_payload import LOGIN_PAYLOAD
import pytest

pytestmark = pytest.mark.api


@pytest.mark.regression
def test_login_without_email(reqres_request_context):
    invalid_payload = {
        "project_id": LOGIN_PAYLOAD["project_id"]
    }

    response = reqres_request_context.post(
        "app-users/login",
        data=invalid_payload
    )

    assert response.status == 400

    response_body = response.json()

    assert response_body["error"] == "email is required"


@pytest.mark.regression
def test_login_with_empty_email(reqres_request_context):
    invalid_payload = {
        "project_id": LOGIN_PAYLOAD["project_id"],
        "email": ""
    }

    response = reqres_request_context.post(
        "app-users/login",
        data=invalid_payload
    )

    assert response.status == 400

    response_body = response.json()

    assert response_body["error"] == "email is required"


@pytest.mark.regression
def test_login_with_invalid_email_format(reqres_request_context):
    invalid_payload = {
        "project_id": LOGIN_PAYLOAD["project_id"],
        "email": "abc"
    }

    response = reqres_request_context.post(
        "app-users/login",
        data=invalid_payload
    )

    assert response.status == 400

    response_body = response.json()

    assert response_body["error"] == "invalid_email"
    assert response_body["message"] == "Provide a valid email address."


@pytest.mark.regression
def test_missing_api_key(playwright, reqres_base_url):
    request = playwright.request.new_context(
        base_url=reqres_base_url,
        extra_http_headers={
            "X-Reqres-Env": "dev"
        }
    )

    try:
        response = request.get("collections/products/records")

        assert response.status == 401, (
            f"Expected 401, got {response.status}. "
            f"Body: {response.text()}"
        )
    finally:
        request.dispose()


@pytest.mark.regression
def test_invalid_api_key(playwright, reqres_base_url):
    request = playwright.request.new_context(
        base_url=reqres_base_url,
        extra_http_headers={
            "x-api-key": "invalid-api-key",
            "X-Reqres-Env": "dev"
        }
    )

    try:
        response = request.get("collections/products/records")

        assert response.status == 403, (
            f"Expected 403, got {response.status}. "
            f"Body: {response.text()}"
        )
    finally:
        request.dispose()


@pytest.mark.regression
def test_login_with_reserved_email(reqres_request_context):
    payload = {
        "project_id": LOGIN_PAYLOAD["project_id"],
        "email": "invalid-project@example.com"
    }

    response = reqres_request_context.post(
        "app-users/login",
        data=payload
    )

    assert response.status == 400

    response_body = response.json()
    assert response_body["error"] == "undeliverable_email"