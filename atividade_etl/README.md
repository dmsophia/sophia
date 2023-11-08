# Atividade de ETL na API da Open Weather

Este serviço foi desenvolvido para extrair, transformar e carregar (ETL) dados climáticos de 10 cidades específicas a partir da API do OpenWeatherMap e fornecer uma interface para acessar esses dados por meio de uma aplicação web Flask. Também inclui um conjunto de testes para garantir a funcionalidade do processo ETL e dos endpoints da API.

## Recursos

- **ETL de Dados Climáticos:** A classe `WeatherETL` gerencia o processo ETL. Ela extrai dados climáticos atuais da API do OpenWeatherMap para uma lista predefinida de cidades `('São Paulo', 'Rio de Janeiro', 'Salvador', 'Fortaleza', 'Belo Horizonte', 'Pernambuco', 'Santa Catarina', 'Porto Alegre', 'Natal', 'Vitória')`, transforma esses dados e os carrega em um banco de dados SQLite chamado `clima.db`.
- **Endpoints da API:** O serviço oferece dois endpoints principais. O endpoint `/etl` executa o processo ETL e o endpoint `/data` retorna os dados climáticos armazenados no banco de dados.
- **Testes Automatizados:** Inclui testes para verificar se a rota ETL está operacional e se os dados podem ser recuperados conforme esperado.

## Como Rodar o Serviço

1. **Instalação das Dependências:**
   Antes de iniciar o serviço, é necessário instalar todas as dependências necessárias usando o pip:

   ```sh
   pip install -r requirements.txt
   ```

2. **Configuração do Ambiente:**
   Você deve ter o Flask e outras bibliotecas necessárias instaladas, além de ter acesso a uma chave válida da API do OpenWeatherMap, que deve ser inserida no lugar do valor `API_KEY` na classe `WeatherETL`. Para caso do exercício, já foi estabelecida uma API_KEY funcional diretamente no código. Por fim, deve instalar o SQLite com o comando: (Caso seu sistema operacional seja Linux.)

   ```sh
   sudo apt install sqlite3
   ```

3. **Inicializando o Banco de Dados:**
   A classe `WeatherETL` irá criar a tabela necessária no banco de dados SQLite se ela ainda não existir. Este passo é automatizado e ocorrerá durante o primeiro lançamento do serviço.

4. **Executando a Aplicação:**
   Para iniciar o servidor Flask, execute:

   ```sh
   flask run
   ```

   Por padrão, o serviço estará disponível em `http://127.0.0.1:5000`.

## Endpoints da API

- **GET `/etl`:** Dispara o processo ETL, atualizando o banco de dados com os dados climáticos mais recentes.
- **GET `/data`:** Recupera todos os dados climáticos armazenados no banco de dados e os retorna em formato JSON.

## Testando a Aplicação

Para rodar os testes e garantir que tudo está funcionando como esperado, execute:

```sh
pytest
```

Os testes vão verificar se o processo ETL está operacional e se os dados podem ser recuperados corretamente.

Também é possível acessar e testar as rotas em aplicações como o Postman. Para isso, selecione o método `GET` no dropdown e coloque `http://127.0.0.1:5000` + `/etl` ou `/data`
