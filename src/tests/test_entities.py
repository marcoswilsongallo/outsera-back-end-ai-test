import pytest
from Domain.entities import GoldenRaspberryAwards

@pytest.fixture
def awards_service():
    return GoldenRaspberryAwards()

def test_wostmovies_returns_list(awards_service):
    movies = awards_service.wostmovies()
    assert isinstance(movies, list)

def test_input_update_delete_movie(awards_service):
    # Test Inserção
    inserted = awards_service.input_movie(
        year=2026,
        title="Test Movie",
        studios="Test Studio",
        producers="Test Producer",
        winner="yes"
    )
    assert inserted is True

    movies = awards_service.wostmovies()
    test_movie = next((m for m in movies if m["title"] == "Test Movie"), None)
    assert test_movie is not None

    # Test Update
    updated = awards_service.update_movie(test_movie["id"], {"title": "Test Movie Updated"})
    assert updated is True

    # Test Delete
    deleted = awards_service.delete_movie(test_movie["id"])
    assert deleted is True

def test_interval_two_awards(awards_service):
    intervals = awards_service.IntervalTwoAwards()
    assert isinstance(intervals, list)

def test_producer_longest_interval(awards_service):
    dummy_data = [
        {"producer": "Producer A", "interval": 1, "previousWin": 1990, "followingWin": 1991},
        {"producer": "Producer B", "interval": 10, "previousWin": 2000, "followingWin": 2010}
    ]
    longest = awards_service.ProducerLongestIntervalTwoAwards(dummy_data)
    assert len(longest) == 1
    assert longest[0]["producer"] == "Producer B"

def test_producer_shortest_interval(awards_service):
    dummy_data = [
        {"producer": "Producer A", "interval": 1, "previousWin": 1990, "followingWin": 1991},
        {"producer": "Producer B", "interval": 10, "previousWin": 2000, "followingWin": 2010}
    ]
    shortest = awards_service.ProducerShortestIntervalTwoAwards(dummy_data)
    assert len(shortest) == 1
    assert shortest[0]["producer"] == "Producer A"