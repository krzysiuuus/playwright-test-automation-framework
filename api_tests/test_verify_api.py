def test_verify_with_invalid_magic_token(reqres_request_context):
    invalid_payload = {
        "token": "invalid-token"
    }

    response = reqres_request_context.post(
        "app-users/verify",
        data=invalid_payload
    )

    assert response.status == 400

    response_body = response.json()

    assert response_body["error"] == "invalid_token"
    assert response_body["message"] == "Token not found"


def test_verify_without_token(reqres_request_context):
    response = reqres_request_context.post(
        "app-users/verify",
        data={}
    )

    assert response.status == 400

    response_body = response.json()

    assert response_body["error"] == "token is required"


def test_verify_with_empty_token(reqres_request_context):
    response = reqres_request_context.post(
        "app-users/verify",
        data={
            "token": ""
        }
    )

    assert response.status == 400

    response_body = response.json()

    assert response_body["error"] == "token is required"


def test_verify_with_invalid_token_type(reqres_request_context):
    response = reqres_request_context.post(
        "app-users/verify",
        data={
            "token": 12345
        }
    )

    assert response.status == 400

    response_body = response.json()

    assert response_body["error"] == "invalid_token"
    assert response_body["message"] == "Token not found"