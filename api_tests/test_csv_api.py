import csv
from io import StringIO


def test_csv_parsing():
    csv_data = """id,name,role
1,John,Tester
2,Anna,Developer
"""

    reader = csv.DictReader(StringIO(csv_data))

    assert reader.fieldnames == ["id", "name", "role"]

    rows = list(reader)

    assert len(rows) == 2
    assert rows[0]["name"] == "John"
    assert rows[0]["role"] == "Tester"
    assert int(rows[1]["id"]) == 2


def test_csv_with_semicolon_delimiter():
    csv_data = """id;name;role
1;John;Tester
2;Anna;Developer
"""

    reader = csv.DictReader(
        StringIO(csv_data),
        delimiter=";"
    )

    assert reader.fieldnames == ["id", "name", "role"]

    rows = list(reader)

    assert len(rows) == 2
    assert rows[1]["name"] == "Anna"


def test_csv_response_from_api(api_request_context):
    response = api_request_context.get(
        "https://raw.githubusercontent.com/apache/spark/master/examples/src/main/resources/people.csv"
    )

    assert response.status == 200

    csv_text = response.text()

    reader = csv.DictReader(
        StringIO(csv_text),
        delimiter=";"
    )

    assert reader.fieldnames == ["name", "age", "job"]

    rows = list(reader)

    assert len(rows) == 2
    assert rows[0]["name"] == "Jorge"
    assert int(rows[0]["age"]) == 30
    assert rows[0]["job"] == "Developer"

    assert rows[1]["name"] == "Bob"
    assert int(rows[1]["age"]) == 32


def test_csv_missing_required_column():
    csv_data = """id,name
1,John
2,Anna
"""

    reader = csv.DictReader(StringIO(csv_data))

    required_columns = ["id", "name", "role"]

    # assert if columns match
    # assert all(column in reader.fieldnames for column in required_columns)

    missing_columns = [
        column
        for column in required_columns
        if column not in reader.fieldnames
    ]

    assert missing_columns == ["role"]


def test_csv_empty_required_value():
    csv_data = """id,name,role
1,John,Tester
2,,Developer
"""

    reader = csv.DictReader(StringIO(csv_data))
    rows = list(reader)

    assert rows[1]["name"] == ""

    required_fields = ["id", "name", "role"]

    invalid_rows = []

    for index, row in enumerate(rows, start=1):
        for field in required_fields:
            if row[field] == "":
                invalid_rows.append((index, field))

    assert invalid_rows == [(2, "name")]


def test_csv_invalid_numeric_value():
    csv_data = """id,name,role
1,John,Tester
abc,Anna,Developer
"""

    reader = csv.DictReader(StringIO(csv_data))
    rows = list(reader)

    invalid_ids = []

    for index, row in enumerate(rows, start=1):
        try:
            int(row["id"])
        except ValueError:
            invalid_ids.append((index, row["id"]))

    assert invalid_ids == [(2, "abc")]