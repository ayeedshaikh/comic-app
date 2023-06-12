import pytest
import connexion

app = connexion.App(__name__, specification_dir='../')
app.add_api('swagger.yml')

@pytest.fixture
def client():
    with app.app.test_client() as client:
        yield client

def test_get_comic_by_id(client):
    response = client.post(f"/comic-by-id/2787")
    assert response.status_code == 200
    assert response.json == {
        "image_url": "https://imgs.xkcd.com/comics/iceberg.png",
        "title": "Iceberg"
    }

def test_get_comic_by_date(client):
    response = client.post(f"/comic-by-id/09062023")
    assert response.status_code == 200
    assert response.json == {
        "image_url": "https://imgs.xkcd.com/comics/iceberg.png",
        "title": "Iceberg"
    }

def test_search_comic_by_date(client):
    response = client.post(f"/comic-by-id/09062023")
    assert response.status_code == 200
    assert response.json == {
        "image_url": "https://imgs.xkcd.com/comics/iceberg.png",
        "title": "Iceberg"
    }

def test_get_comic_statistics(client):
    response = client.post(f"/comic-by-id/2787")
    assert response.status_code == 200
    assert response.json == {
        "image_url": "https://imgs.xkcd.com/comics/iceberg.png",
        "title": "Iceberg",
        "views": 1
    }