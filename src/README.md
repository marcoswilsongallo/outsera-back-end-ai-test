# Golden Raspberry Awards - REST API (Outsera Back-End Test)

Projeto de microserviço RESTful desenvolvido em **Python 3.13** e **Flask**, seguindo os princípios de **Clean Architecture**. A aplicação analisa os indicados e vencedores da categoria _Pior Filme_ do **Golden Raspberry Awards** (Framboesa de Ouro), permitindo a consulta dos produtores com os maiores e menores intervalos entre prêmios consecutivos, além de oferecer endpoints CRUD para gestão dos filmes.

## 1\. Visão Geral da Arquitetura

A estrutura do projeto respeita a divisão em camadas para garantir baixo acoplamento e facilidade de manutenção:

- src/app.py: Ponto de entrada (Bootstrapper) da aplicação Flask executada no host local na porta 5000.
- src/infrastructure/: Contém a camada de persistência com **SQLite** (MovieList.db) via **SQLAlchemy** (database.py), carga automática do arquivo Movielist.csv e a classe DTO de dados (IntervalTimeAwards.py).
- src/Domain/: Regras de negócio em entities.py (agrupamento de produtores, ordenação por ano, cálculo de intervalos e identificação de maior/menor intervalo).
- src/Routes/: Definição das rotas REST em routes.py com suporte a **Rate Limiting** (20 requisições por 10 segundos com _sleep and retry_).
- src/tests/: Suíte de testes unitários (test_entities.py) e testes de integração (test_integration.py).

## 2\. Pré-requisitos e Instalação

### Pré-requisitos

- Python 3.13 ou superior instalado.
- Arquivo Movielist.csv posicionado no diretório: C:\\Sistemas\\teste-outsera-python\\outsera-back-end-ai-test\\src\\infrastructure\\Movielist.csv

### Instalação das Dependências

Navegue até a pasta raiz e instale as bibliotecas listadas no requirements.txt:

```
cd /d C:\Sistemas\teste-outsera-python\outsera-back-end-ai-test-github
pip install -r src\requirements.txt
```

## 3\. Como Iniciar a Aplicação

Para executar o servidor Flask localmente na porta 5000:

```
cd /d C:\Sistemas\teste-outsera-python\outsera-back-end-ai-test
python src\app.py
```

_Nota: Na primeira execução, o banco de dados SQLite MovieList.db será automaticamente criado no diretório src\\infrastructure\\ e populado com os dados provenientes do Movielist.csv._

## 4\. Guia de Endpoints da API
http://127.0.0.1:5000/goldenraspberryawards/wostmovies
http://127.0.0.1:5000/goldenraspberryawards/LongestTwoAwards
http://127.0.0.1:5000/goldenraspberryawards/shortestTwoAwards

| **Método** | **Rota**                                 | **Descrição**                                                                        |
| ---------- | ---------------------------------------- | ------------------------------------------------------------------------------------ |
| **GET**    | /goldenraspberryawards/wostmovies        | Retorna a lista completa de todos os filmes gravados na tabela Movies.               |
| **GET**    | /goldenraspberryawards/LongestTwoAwards  | Retorna o(s) produtor(es) com o **maior intervalo** entre dois prêmios consecutivos. |
| **GET**    | /goldenraspberryawards/shortestTwoAwards | Retorna o(s) produtor(es) com o **menor intervalo** entre dois prêmios consecutivos. |
| **POST**   | /goldenraspberryawards/movies            | Cadastra um novo filme no banco de dados.                                            |
| **PUT**    | /goldenraspberryawards/movies            | Atualiza os dados de um filme existente informando o id.                             |
| **DELETE** | /goldenraspberryawards/movies            | Remove um filme cadastrado informando o id.                                          |

### Exemplos de Payload (JSON)

#### Criar Filme (POST)

```
POST /goldenraspberryawards/movies
Content-Type: application/json

{
  "year": 2024,
  "title": "Example Movie",
  "studios": "Example Studio",
  "producers": "John Doe and Jane Doe",
  "winner": "yes"
}
```

#### Atualizar Filme (PUT)

```
PUT /goldenraspberryawards/movies
Content-Type: application/json

{
  "id": 1,
  "title": "Updated Title",
  "winner": "no"
}
```

#### Deletar Filme (DELETE)

```
DELETE /goldenraspberryawards/movies
Content-Type: application/json

{
  "id": 1
}
```

## 5\. Execução dos Testes

Os testes abrangem validações unitárias da lógica do domínio e testes de integração end-to-end das rotas com os dados do CSV.

### Executar Todos os Testes

```
cd /d C:\Sistemas\teste-outsera-python\outsera-back-end-ai-test
pytest src/tests/
```

### Executar Apenas Testes Unitários

```
pytest src/tests/test_entities.py
```

### Executar Apenas Testes de Integração

```
pytest src/tests/test_integration.py
```

## 6\. Arquivos Gerados no Projeto

Abaixo está a estrutura de arquivos final organizada:

```
outsera-back-end-ai-test/
├── README.md
└── src/
    ├── __init__.py
    ├── app.py
    ├── requirements.txt
    ├── Domain/
    │   ├── __init__.py
    │   └── entities.py
    ├── Routes/
    │   ├── __init__.py
    │   └── routes.py
    ├── infrastructure/
    │   ├── __init__.py
    │   ├── database.py
    │   ├── IntervalTimeAwards.py
    │   ├── Movielist.csv
    │   └── MovieList.db
    └── tests/
        ├── __init__.py
        ├── test_entities.py
        └── test_integration.py
```