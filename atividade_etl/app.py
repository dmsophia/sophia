from flask import Flask, jsonify, g
import requests
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(WeatherETL.DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

class WeatherETL:
    DATABASE = 'clima.db'
    API_KEY = '2c6612dc25ba49da5240a19ee4d0621d'
    CITIES = ['Sao Paulo', 'Rio de Janeiro', 'Salvador', 'Fortaleza', 'Belo Horizonte', 'Pernambuco', 'Santa Catarina', 'Porto Alegre', 'Natal', 'Vitória']
    
    def __init__(self):
        self.init_db()
    
    def init_db(self):
        with sqlite3.connect(self.DATABASE) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS clima (
                    data_ingestao TEXT,
                    tipo TEXT,
                    valores REAL,
                    uso TEXT
                )
            ''')
            conn.commit()
    
    def run_etl(self):
        for city in self.CITIES:
            weather_data = self.get_weather_data(city)
            self.insert_weather_data(weather_data, city)
        return {'message': 'ETL executado com sucesso.'}

    def get_weather_data(self, city):
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={self.API_KEY}&units=metric"
        response = requests.get(base_url)
        return response.json()

    def insert_weather_data(self, data, city):
        with sqlite3.connect(self.DATABASE) as conn:
            c = conn.cursor()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            temperature = data.get('main', {}).get('temp')
            usage = 'previsão'
            c.execute('INSERT INTO clima (data_ingestao, tipo, valores, uso) VALUES (?, ?, ?, ?)',
                      (timestamp, city, temperature, usage))
            conn.commit()

    @staticmethod
    def get_all_weather_data():
        cursor = get_db().cursor()
        cursor.execute('SELECT * FROM clima')
        rows = cursor.fetchall()
        return [dict(row) for row in rows]  # Convert rows to dictionaries

etl_processor = WeatherETL()

@app.route('/etl')
def etl_route():
    result = etl_processor.run_etl()
    return jsonify(result)

@app.route('/data', methods=['GET'])
def get_data():
    data = etl_processor.get_all_weather_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
