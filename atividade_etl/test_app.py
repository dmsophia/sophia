import pytest
from app import app, WeatherETL, get_db
import requests_mock
import sqlite3

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            init_db() 
        yield client

def init_db():
    with sqlite3.connect(WeatherETL.DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS clima (
                data_ingestao TEXT,
                tipo TEXT,
                valores REAL,
                uso TEXT
            )
        ''')
        conn.commit()

def test_etl_route(client):
    with requests_mock.Mocker() as m:
        for city in WeatherETL.CITIES:
            m.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={WeatherETL.API_KEY}&units=metric",
                  json={'main': {'temp': 25}})
        
        response = client.get('/etl')
        
        assert response.status_code == 200
        assert response.json == {'message': 'ETL executado com sucesso.'}

def test_data_route(client):
    # Clear the database table before inserting test data
    with sqlite3.connect(WeatherETL.DATABASE) as conn:
        conn.execute('DELETE FROM clima')
        conn.commit()

        conn.execute('INSERT INTO clima (data_ingestao, tipo, valores, uso) VALUES (?, ?, ?, ?)',
                     ("2023-01-01 12:00:00", "Test City", 20.0, "previsão"))
        conn.commit()
    
    response = client.get('/data')
    
    assert response.status_code == 200
    data = response.json
    assert len(data) == 1  
    assert data[0]['tipo'] == "Test City"
    assert data[0]['valores'] == 20.0
    assert data[0]['uso'] == "previsão"

@pytest.fixture(scope="module")
def teardown():
    yield
    with sqlite3.connect(WeatherETL.DATABASE) as conn:
        conn.execute('DROP TABLE clima')
        conn.commit()
