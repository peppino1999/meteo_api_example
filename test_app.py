import pytest
from app import app, CITIES

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

class TestIndex:
    def test_index_returns_api_info(self, client):
        response = client.get('/')
        data = response.get_json()
        
        assert response.status_code == 200
        assert 'message' in data
        assert 'endpoints' in data
        assert 'available_cities' in data

class TestWeatherByCity:
    def test_weather_rome(self, client):
        response = client.get('/weather/rome')
        data = response.get_json()
        
        assert response.status_code == 200
        assert data['city'] == 'Rome'
        assert 'current' in data
        assert 'daily' in data

    def test_weather_milan(self, client):
        response = client.get('/weather/milan')
        data = response.get_json()
        
        assert response.status_code == 200
        assert data['city'] == 'Milan'

    def test_weather_unknown_city(self, client):
        response = client.get('/weather/unknown')
        data = response.get_json()
        
        assert response.status_code == 404
        assert 'error' in data

class TestWeatherByParams:
    def test_weather_with_city_param(self, client):
        response = client.get('/weather?city=rome')
        data = response.get_json()
        
        assert response.status_code == 200
        assert data['city'] == 'rome'

    def test_weather_with_coords(self, client):
        response = client.get('/weather?lat=41.9&lon=12.5')
        data = response.get_json()
        
        assert response.status_code == 200

    def test_weather_default(self, client):
        response = client.get('/weather')
        data = response.get_json()
        
        assert response.status_code == 200

class TestCities:
    def test_all_cities_available(self):
        expected_cities = ['rome', 'milan', 'naples', 'turin', 'palermo', 
                          'genoa', 'bologna', 'florence', 'bari', 'catania']
        
        for city in expected_cities:
            assert city in CITIES

    def test_city_coordinates(self):
        assert CITIES['rome']['lat'] == 41.9028
        assert CITIES['rome']['lon'] == 12.4964