import io
import pytest

from web_app.app import app

@pytest.fixture
def client():

    # allow test failures to show full tracebacks
    app.config["TESTING"] = True

    # simulate HTTPS request 
    with app.test_client() as client:
        yield client

# GET Route Tests

def test_index_get_returns_200(client):

    # page load should return 200 OK response
    response = client.get("/")

    assert response.status_code == 200


def test_rules_builder_get_returns_200(client):

    response = client.get("/rules-builder")

    assert response.status_code == 200


# POST Error Tests
def test_upload_post_with_no_file_field_returns_error(client):

    # submitted form with no file field should return error
    response = client.post("/upload", data={})

    assert response.status_code == 200
    assert b"No file field was submitted" in response.data


def test_upload_post_with_no_valid_csv_returns_error(client):

    # submitted form with non-CSV file should return error
    fake_file = (io.BytesIO(b"some content"), "document.txt")

    response = client.post(
        "/upload",
        data={"csv_files": fake_file},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert b"No valid CSV files were selected" in response.data


def test_upload_post_with_invalid_rules_file_returns_error(client):

    # upload of .txt file as rules file should return an error
    csv_file = (io.BytesIO(b"name,age\nAlice,30\n"), "test.csv")
    bad_rules = (io.BytesIO(b"not json"), "rules.txt")

    response = client.post(
        "/upload",
        data={"csv_files": csv_file, "rules_file": bad_rules},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert b"Rules file must be a .json file" in response.data


def test_upload_post_with_valid_csv_returns_report(client):

    # valid CSV upload should render report page
    csv_content = b"name,age\nAlice,30\nBob,25\n"
    csv_file = (io.BytesIO(csv_content), "test.csv")

    response = client.post(
        "/upload",
        data={"csv_files": csv_file},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert b"Batch Summary" in response.data


def test_upload_get_returns_200(client):

    # upload page should load successfully
    response = client.get("/upload")

    assert response.status_code == 200


def test_download_report_nonexistent_file_returns_404(client):

    # requesting a report that doesn't exist should return a 404
    response = client.get("/download-report/nonexistent/report.md")

    assert response.status_code == 404
