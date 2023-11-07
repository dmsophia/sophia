## Visão Geral

Este serviço foi desenvolvido para extrair, transformar e carregar (ETL) dados climáticos de cidades específicas a partir da API do OpenWeatherMap e fornecer uma interface para acessar esses dados por meio de uma aplicação web Flask. Também inclui um conjunto de testes para garantir a funcionalidade do processo ETL e dos endpoints da API.

## Recursos

- **ETL de Dados Climáticos:** A classe `WeatherETL` gerencia o processo ETL. Ela extrai dados climáticos atuais da API do OpenWeatherMap para uma lista predefinida de cidades, transforma esses dados e os carrega em um banco de dados SQLite.
- **Endpoints da API:** O serviço oferece dois endpoints principais. O endpoint `/etl` executa o processo ETL e o endpoint `/data` retorna os dados climáticos armazenados.
- **Testes Automatizados:** Inclui testes para verificar se a rota ETL está operacional e se os dados podem ser recuperados conforme esperado.

## Como Rodar o Serviço

1. **Instalação das Dependências:**
   Antes de iniciar o serviço, é necessário instalar todas as dependências necessárias usando o pip:

   ```sh
   pip install -r requirements.txt
   ```

2. **Configuração do Ambiente:**
   Você deve ter o Flask e outras bibliotecas necessárias instaladas, além de ter acesso a uma chave válida da API do OpenWeatherMap, que deve ser inserida no lugar do valor `API_KEY` na classe `WeatherETL`.

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

## Limpeza e Manutenção

Após os testes ou a execução do serviço, você pode querer remover a tabela do banco de dados. Isso pode ser feito com a fixture `teardown` do pytest que, ao ser executada, excluirá a tabela `clima`.

---

Ao usar este serviço, você estará apto a executar operações ETL de dados climáticos e disponibilizar esses dados por meio de uma API construída com o Flask.