import json
from pathlib import Path
import pytest
from jsonschema import validate, FormatChecker, ValidationError


def test_json_response(api_request_context):
    response = api_request_context.get("/users/1")

    assert response.status == 200
    assert "application/json" in response.headers["content-type"]

    data = response.json()

    schema_path = Path(__file__).parent / "schemas" / "user_schema.json"

    with open(schema_path, "r") as file:
        user_schema = json.load(file)

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
    ]
)
def test_invalid_json_fails_schema_validation(
        invalid_data,
        expected_validator,
        expected_path
):
    schema_path = Path(__file__).parent / "schemas" / "user_schema.json"

    with open(schema_path, "r") as file:
        user_schema = json.load(file)

    with pytest.raises(ValidationError) as error:
        validate(
            instance=invalid_data,
            schema=user_schema,
            format_checker=FormatChecker()
        )

    assert error.value.validator == expected_validator
    assert list(error.value.path) == expected_path