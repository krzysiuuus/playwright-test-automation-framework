import yaml
import pytest
import yaml


def test_yaml_parsing():
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


def test_yaml_nested_structure():
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

    assert data["environment"]["name"] == "test"
    assert data["environment"]["retries"] == 3
    assert len(data["environment"]["browsers"]) == 3
    assert data["environment"]["browsers"][1] == "firefox"

    database = data["environment"]["database"]

    assert database["host"] == "localhost"
    assert database["port"] == 5432
    assert database["enabled"] is True


def test_invalid_yaml_indentation():
    invalid_yaml = """
    user:
      name: John
        active: true
    """

    with pytest.raises(yaml.YAMLError):
        yaml.safe_load(invalid_yaml)