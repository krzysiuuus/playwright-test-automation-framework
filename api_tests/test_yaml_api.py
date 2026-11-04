import yaml
import pytest


def test_yaml_user_data_has_expected_structure():
    yaml_data = """
    user:
      id: 1
      name: John
      active: true
      roles:
        - tester
        - admin
    """

    data = yaml.safe_load(yaml_data)

    assert data["user"]["id"] == 1
    assert data["user"]["name"] == "John"
    assert data["user"]["active"] is True
    assert data["user"]["roles"][0] == "tester"


def test_yaml_environment_config_has_expected_values():
    yaml_data = """
    environment:
      name: test
      retries: 3
      browsers:
        - chromium
        - firefox
        - webkit
      database:
        host: localhost
        port: 5432
        enabled: true
    """

    data = yaml.safe_load(yaml_data)
    environment = data["environment"]

    assert environment["name"] == "test"
    assert environment["retries"] == 3
    assert len(environment["browsers"]) == 3
    assert environment["browsers"][1] == "firefox"

    database = environment["database"]

    assert database["host"] == "localhost"
    assert database["port"] == 5432
    assert database["enabled"] is True


def test_invalid_yaml_indentation_raises_error():
    invalid_yaml = """
    user:
      name: John
        active: true
    """

    with pytest.raises(yaml.YAMLError):
        yaml.safe_load(invalid_yaml)