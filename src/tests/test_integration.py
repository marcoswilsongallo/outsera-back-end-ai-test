import pytest
from src.app import app
@pytest.fixture
def client():
    #app = app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_all_movies(client):
    response = client.get('/goldenraspberryawards/wostmovies')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_longest_and_shortest_intervals_integration(client):
    response_min = client.get('/goldenraspberryawards/shortestTwoAwards')
    assert response_min.status_code == 200
    data_min = response_min.get_json()
    assert "min" in data_min

    response_max = client.get('/goldenraspberryawards/LongestTwoAwards')
    assert response_max.status_code == 200
    data_max = response_max.get_json()
    assert "max" in data_max

def test_crud_movie_workflow(client):
    # Create
    new_movie = {
        "year": 2026,
        "title": "Test AI Movie",
        "studios": "Outsera Studios",
        "producers": "Test Producer",
        "winner": "yes"
    }
    res_post = client.post('/goldenraspberryawards/movies', json=new_movie)
    assert res_post.status_code == 201

    # Retrieve all to find inserted item
    res_get = client.get('/goldenraspberryawards/wostmovies')
    movies = res_get.get_json()
    inserted = next((m for m in movies if m['title'] == "Test AI Movie"), None)
    assert inserted is not None

    # Update
    res_put = client.put('/goldenraspberryawards/movies', json={"id": inserted["id"], "title": "Test AI Movie Updated"})
    assert res_put.status_code == 200

    # Delete
    res_del = client.delete('/goldenraspberryawards/movies', json={"id": inserted["id"]})
    assert res_del.status_code == 200