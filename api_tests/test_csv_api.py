import csv
from io import StringIO
import pytest

pytestmark = pytest.mark.api

class CsvReaderContext:

    def __init__(self, csv_text):
        self.csv_text = csv_text
        self.file = None

    def __enter__(self):
        self.file = StringIO(self.csv_text)
        return csv.DictReader(self.file)

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()
        return False


@pytest.mark.regression
def test_csv_custom_context_manager():
    csv_data = """id,name,role
1,John,Tester
2,Anna,Developer
"""

    manager = CsvReaderContext(csv_data)

    with manager as reader:
        rows = list(reader)

        assert len(rows) == 2
        assert rows[0]["name"] == "John"

    assert manager.file.closed


def get_rows_by_role(csv_text, role):
    with StringIO(csv_text) as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["role"] == role:
                yield row


@pytest.mark.regression
def test_csv_generator():
    csv_data = """id,name,role
1,John,Tester
2,Anna,Developer
3,Mike,Tester
"""

    rows = get_rows_by_role(csv_data, "Tester")

    assert iter(rows) is rows

    assert next(rows)["name"] == "John"
    assert next(rows)["name"] == "Mike"

    with pytest.raises(StopIteration):
        next(rows)


@pytest.mark.regression
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


@pytest.mark.regression
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


@pytest.mark.regression
def test_csv_response_has_expected_data(github_raw_request_context):
    response = github_raw_request_context.get(
        "/apache/spark/master/examples/src/main/resources/people.csv"
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


@pytest.mark.regression
def test_csv_detects_missing_required_column():
    csv_data = """id,name
1,John
2,Anna
"""

    reader = csv.DictReader(StringIO(csv_data))

    required_columns = ["id", "name", "role"]

    missing_columns = [
        column
        for column in required_columns
        if column not in reader.fieldnames
    ]

    assert missing_columns == ["role"]


@pytest.mark.regression
def test_csv_detects_empty_required_value():
    csv_data = """id,name,role
1,John,Tester
2,,Developer
"""

    reader = csv.DictReader(StringIO(csv_data))
    rows = list(reader)

    required_fields = ["id", "name", "role"]

    invalid_rows = []

    for index, row in enumerate(rows, start=1):
        for field in required_fields:
            if row[field] == "":
                invalid_rows.append((index, field))

    assert invalid_rows == [(2, "name")]


@pytest.mark.regression
def test_csv_detects_invalid_numeric_value():
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