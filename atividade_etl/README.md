# Atividade de ETL na API da Open Weather

Este serviço em Flask realiza a extração, transformação e carga (ETL) de dados climáticos de cidades específicas através da API OpenWeatherMap, armazenando-os em um banco de dados SQLite para fácil acesso e análise.

## Configuração do Flask

Configure a variável de ambiente `FLASK_APP`:

```sh
export FLASK_APP=app.py
```

## Implementação do ETL

A classe `WeatherETL` gerencia o ETL:

- **Extração:** Coleta dados da API OpenWeatherMap.
- **Transformação:** Formata os dados brutos.
- **Carga:** Insere os dados no banco de dados `clima.db`.

## Armazenamento dos Dados

Os dados são armazenados na tabela `weather_data` no banco de dados SQLite `clima.db`.

## Como Rodar o Serviço

1. Instale as dependências:

   ```sh
   pip install -r requirements.txt
   ```

2. Defina sua chave de API da OpenWeather no código.
3. Inicialize o banco de dados:

   ```sh
   python -c 'from app import WeatherETL; WeatherETL.init_db()'
   ```

4. Execute o serviço Flask:

   ```sh
   flask run
   ```

## Endpoints da API

- **GET `/etl`**: Executa o processo ETL.
- **GET `/data`**: Retorna os dados climáticos armazenados.

## Testando a Aplicação

Para testar a aplicação, execute:

```sh
pytest
```

Para interação manual com a API, use o Postman para acessar `http://127.0.0.1:5000/etl` ou `http://127.0.0.1:5000/data`.
