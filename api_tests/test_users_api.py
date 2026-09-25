from playwright.sync_api import expect


def test_get_user(api_request_context):
    response = api_request_context.get("/users/1")

    expect(response).to_be_ok()

    response_body = response.json()

    assert response_body["id"] == 1
    assert response_body["name"] == "Leanne Graham"
    assert response_body["email"] == "Sincere@april.biz"


def test_create_post(api_request_context):
    payload = {
        "title": "Playwright API test",
        "body": "Test automation framework",
        "userId": 1
    }

    response = api_request_context.post(
        "/posts",
        data=payload
    )

    assert response.status == 201

    response_body = response.json()

    assert response_body["title"] == payload["title"]
    assert response_body["body"] == payload["body"]
    assert response_body["userId"] == payload["userId"]