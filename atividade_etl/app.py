from flask import Flask, jsonify, g
import requests
import sqlite3
from datetime import datetime
import json

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('clima.db')
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

class WeatherETL:
    API_KEY = '2c6612dc25ba49da5240a19ee4d0621d'  
    CITIES = ['São Paulo', 'Rio de Janeiro', 'Salvador', 'Fortaleza', 'Belo Horizonte']

    @staticmethod
    def init_db():
        with get_db() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS clima (
                    data_ingestao TEXT,
                    tipo TEXT,
                    valores TEXT,
                    uso TEXT
                )
            ''')
            conn.commit()

    @staticmethod
    def get_weather_data(city):
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={WeatherETL.API_KEY}&units=metric"
        response = requests.get(base_url)
        return response.json()

    @staticmethod
    def transform_data(data, city):
        weather_details = {
            'temperature': data.get('main', {}).get('temp'),
            'humidity': data.get('main', {}).get('humidity'),
            'pressure': data.get('main', {}).get('pressure'),
            'description': data.get('weather', [{}])[0].get('description')
        }
        values = json.dumps(weather_details)
        return {
            'data_ingestao': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'tipo': city,
            'valores': values,
            'uso': 'previsão'
        }

    @staticmethod
    def load_data(transformed_data):
        with get_db() as conn:
            conn.execute('INSERT INTO clima (data_ingestao, tipo, valores, uso) VALUES (?, ?, ?, ?)',
                         (transformed_data['data_ingestao'], transformed_data['tipo'],
                          transformed_data['valores'], transformed_data['uso']))
            conn.commit()

    @staticmethod
    def run_etl():
        for city in WeatherETL.CITIES:
            raw_data = WeatherETL.get_weather_data(city)
            if raw_data:
                transformed_data = WeatherETL.transform_data(raw_data, city)
                WeatherETL.load_data(transformed_data)
        return {'message': 'ETL executado com sucesso.'}

@app.route('/etl')
def etl_route():
    result = WeatherETL.run_etl()
    return jsonify(result)

@app.route('/data', methods=['GET'])
def get_data():
    cursor = get_db().cursor()
    cursor.execute('SELECT * FROM clima')
    rows = cursor.fetchall()
    data = []
    for row in rows:
        try:
            valores = json.loads(row["valores"]) if isinstance(row["valores"], str) else row["valores"]
        except (TypeError, ValueError):
            valores = {}  # ou algum valor padrão ou manipulação de erro
        data.append({
            "data_ingestao": row["data_ingestao"],
            "tipo": row["tipo"],
            "uso": row["uso"],
            "valores": valores
        })
    return jsonify(data)

if __name__ == '__main__':
    WeatherETL.init_db()
    app.run(debug=True)
