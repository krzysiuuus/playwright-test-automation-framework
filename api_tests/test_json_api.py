import json
from pathlib import Path
import pytest
from jsonschema import validate, FormatChecker, ValidationError, Draft7Validator


@pytest.fixture(scope="module")
def user_schema():
    schema_path = Path(__file__).parent / "schemas" / "user_schema.json"

    with open(schema_path, "r") as file:
        schema = json.load(file)

    Draft7Validator.check_schema(schema)

    return schema


def test_user_response_matches_schema(api_request_context, user_schema):
    response = api_request_context.get("/users/1")

    assert response.status == 200
    content_type = response.headers.get("content-type", "")

    assert "application/json" in content_type

    data = response.json()

    validate(
        instance=data,
        schema=user_schema,
        format_checker=FormatChecker()
    )

    assert data["id"] == 1


@pytest.mark.parametrize(
    "invalid_data, expected_validator, expected_path",
    [
        (
            {
                "id": "1",
                "name": "John",
                "email": "john@example.com",
                "address": {
                    "street": "Main Street",
                    "city": "Warsaw",
                    "zipcode": "00-001"
                }
            },
            "type",
            ["id"]
        ),
        (
            {
                "id": 1,
                "name": "John",
                "address": {
                    "street": "Main Street",
                    "city": "Warsaw",
                    "zipcode": "00-001"
                }
            },
            "required",
            []
        ),
        (
            {
                "id": 1,
                "name": "John",
                "email": "not-an-email",
                "address": {
                    "street": "Main Street",
                    "city": "Warsaw",
                    "zipcode": "00-001"
                }
            },
            "format",
            ["email"]
        )
    ],
    ids=[
        "invalid-id-type",
        "missing-email",
        "invalid-email-format"
    ]
)
def test_invalid_user_data_fails_schema_validation(
        invalid_data,
        expected_validator,
        expected_path,
        user_schema
):

    with pytest.raises(ValidationError) as error:
        validate(
            instance=invalid_data,
            schema=user_schema,
            format_checker=FormatChecker()
        )

    assert error.value.validator == expected_validator
    assert list(error.value.path) == expected_path