import allure

from api_tests.data.auth_payload import LOGIN_PAYLOAD


@allure.feature("Authentication API")
@allure.title("Verify login request")
def test_authenticated_user_can_access_profile(reqres_request_context, session_token):
    me_response = reqres_request_context.get(
        "app-users/me",
        headers={"Authorization": f"Bearer {session_token}"}
    )

    assert me_response.status == 200

    me_body = me_response.json()

    assert me_body["data"]["email"] == LOGIN_PAYLOAD["email"]
    assert me_body["data"]["project_id"] == LOGIN_PAYLOAD["project_id"]
    assert me_body["data"]["status"] == "active"


def test_profile_access_without_token(reqres_request_context):
    response = reqres_request_context.get("app-users/me")

    assert response.status == 401

    response_body = response.json()

    assert response_body["error"] == "missing_bearer_token"


def test_profile_access_with_invalid_token(reqres_request_context):
    response = reqres_request_context.get(
        "app-users/me",
        headers={"Authorization": "Bearer invalid-token"}
    )

    assert response.status == 401

    response_body = response.json()

    assert response_body["error"] == "invalid_session"


def test_profile_access_with_wrong_auth_scheme(reqres_request_context):
    response = reqres_request_context.get(
        "app-users/me",
        headers={"Authorization": "Basic invalid-token"}
    )

    assert response.status == 401

    response_body = response.json()

    assert response_body["error"] == "missing_bearer_token"


# def test_reqres_api_key(reqres_request_context):
#     response = reqres_request_context.get("users/2")
#
#     print(response.status)
#     print(response.text())
#
#     assert response.status == 200