# Atividade de ETL na API da Open Weather

Este serviço foi desenvolvido para extrair, transformar e carregar (ETL) dados climáticos das seguintes cidades: São Paulo, Rio de Janeiro, Salvador, Fortaleza e Belo Horizonte, a partir da API do OpenWeatherMap. Uma interface Flask permite acessar os dados coletados. O serviço inclui testes automatizados para validar o funcionamento do ETL e dos endpoints da API.

## Recursos

- **ETL de Dados Climáticos:** A classe `WeatherETL` gerencia o ETL, utilizando a API do OpenWeatherMap para extrair dados das cidades mencionadas e armazená-los em `clima.db` do SQLite3.
- **Endpoints da API:** Dois endpoints principais são fornecidos: `/etl` para executar o ETL e `/data` para acessar/visualizar os dados armazenados.

## Como Rodar o Serviço

1. Instale as dependências com `pip install -r requirements.txt`.
2. Certifique-se de ter acesso a uma chave API do OpenWeatherMap para `API_KEY`.
3. Inicialize o banco de dados com `WeatherETL.init_db()`.
4. Execute o serviço com `flask run`.

## Endpoints da API

- **GET `/etl`:** Executa o ETL e atualiza o banco de dados.
- **GET `/data`:** Retorna os dados climáticos armazenados.

## Testando a Aplicação

Execute `pytest` para rodar os testes. Eles verificarão a operacionalidade do ETL e a correta recuperação dos dados.

Acesse `http://127.0.0.1:5000/etl` ou `http://127.0.0.1:5000/data` para testar os endpoints manualmente em alguma aplicação, como o Postman.
