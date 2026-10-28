from api_tests.data.auth_payload import LOGIN_PAYLOAD


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


def test_login_without_api_key(playwright, reqres_base_url):
    request = playwright.request.new_context(
        base_url=reqres_base_url,
        extra_http_headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Reqres-Env": "dev"
        }
    )

    response = request.post(
        "app-users/login",
        data=LOGIN_PAYLOAD
    )

    assert response.status == 404

    response_body = response.json()

    assert response_body["error"] == "Project not found or not accessible"
    assert response_body["message"] == "Provide the project API key or use an owner session."

    request.dispose()


def test_login_with_invalid_api_key(playwright, reqres_base_url):
    request = playwright.request.new_context(
        base_url=reqres_base_url,
        extra_http_headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-api-key": "invalid-api-key",
            "X-Reqres-Env": "dev"
        }
    )

    response = request.post(
        "app-users/login",
        data=LOGIN_PAYLOAD
    )

    assert response.status == 404

    response_body = response.json()

    assert response_body["error"] == "Project not found or not accessible"
    assert response_body["message"] == "Provide the project API key or use an owner session."

    request.dispose()


def test_login_with_invalid_project_id(reqres_request_context):
    invalid_payload = {
        "project_id": 999999,
        "email": LOGIN_PAYLOAD["email"]
    }

    response = reqres_request_context.post(
        "app-users/login",
        data=invalid_payload
    )

    assert response.status == 403

    response_body = response.json()

    assert response_body["error"] == "project_mismatch"
    assert response_body["message"] == "The provided project_id does not match the API key scope."
