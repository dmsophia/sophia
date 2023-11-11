import pytest
from app import app, WeatherETL, get_db
import sqlite3
import json
import requests_mock
from datetime import datetime

@pytest.fixture(scope='module')
def client():
    app.config['TESTING'] = True
    with app.app_context():
        WeatherETL.init_db()
        yield app.test_client()
    with app.app_context():
        with sqlite3.connect('clima.db') as conn:
            conn.execute('DROP TABLE IF EXISTS clima')

@pytest.fixture
def setup_database():
    with app.app_context():
        WeatherETL.init_db()
        yield
        with sqlite3.connect('clima.db') as conn:
            conn.execute('DROP TABLE IF EXISTS clima')

@pytest.fixture
def mock_requests():
    with requests_mock.Mocker() as m:
        yield m

def test_etl_route(client, setup_database, mock_requests):
    for city in WeatherETL.CITIES:
        mock_requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WeatherETL.API_KEY}&units=metric",
                          json={
                              'main': {'temp': 25},
                              'weather': [{'main': 'Clear', 'description': 'clear sky'}]
                          })
    
    response = client.get('/etl')
    assert response.status_code == 200
    assert response.get_json() == {'message': 'ETL executado com sucesso.'}

def test_data_route(client, setup_database):
    with app.app_context():
        conn = get_db()
        conn.execute('DELETE FROM clima')

        weather_details = {
            'temperature': 20,
            'humidity': 50,
            'pressure': 1012,
            'description': 'clear sky'
        }
        transformed_data = {
            'data_ingestao': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'tipo': 'TestCity',
            'valores': json.dumps(weather_details), 
            'uso': 'previsão'
        }
        WeatherETL.load_data(transformed_data)

    response = client.get('/data')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['tipo'] == 'TestCity'
    assert data[0]['uso'] == 'previsão'
    
    assert isinstance(data[0]['valores'], dict), "Valores should be a dictionary"
    assert data[0]['valores'] == weather_details, "The weather details do not match"