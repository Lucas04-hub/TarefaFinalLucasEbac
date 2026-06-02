# API Pokémons - Projeto Final EBAC
API backend desenvolvida com FastAPI, consumindo dados em tempo real da PokéAPI. Exibe listas de pokémons paginadas e detalhes filtrados via endpoints REST.

## Como rodar localmente
# Clone o projeto e acesse a pasta correta
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# Acesse http://127.0.0.1:8000/docs

## Como rodar os testes
pytest

## Link em produção (deploy)
https://tarefafinallucasebac.onrender.com

## Exemplos de uso

### Listar pokémons (paginação)
GET /pokemons?limit=10&offset=0

## Como rodar com Docker e Docker Compose (Podman)
1. Certifique-se de que [Docker ou Podman] e [docker-compose ou podman-compose] estão instalados.
2. Na pasta do projeto, execute:

3. Acesse a API em http://localhost:8000

> Para parar os containers:
>
> ```
> podman-compose down
> ```

## Variáveis de ambiente

- As principais variáveis de ambiente já estão configuradas automaticamente via docker-compose.yml, como:
  - `DATABASE_URL`: string de conexão ao banco de dados PostgreSQL.
- Para rodar localmente sem Compose, ajuste a variável DATABASE_URL conforme a instalação do seu banco.

## Documentação automática dos endpoints

Após iniciar a aplicação, acesse a documentação interativa gerada automaticamente pelo FastAPI em:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc - alternativa)

Nesses links, você pode testar os endpoints da API e ver exemplos de respostas.

## Possíveis problemas ao rodar localmente

- **Porta 5432 ocupada**: Se já houver um PostgreSQL rodando no seu sistema, pare-o antes de subir os containers.
- **Conflito de containers antigos**: Use `podman rm -f $(podman ps -aq)` para limpar containers parados antes de rodar novamente.
- **Variáveis de ambiente de banco**: Garanta que o ambiente esteja limpo para evitar conflitos de conexão.

## Endpoints principais

- GET `/pokemons`: retorna lista paginada de pokémons. Use parâmetros `limit` e `offset`.
  - Exemplo: `/pokemons?limit=10&offset=0`
- GET `/pokemons/{id}`: retorna informações detalhadas de um pokémon.

_Páginação:_ Utilize os parâmetros `limit` e `offset` para navegar entre páginas.

## Funcionalidades extras implementadas
- (Exemplo: Cache com Redis, tratamento de exceções personalizado, etc.)

## Executando os testes

Após instalar as dependências ou subir o ambiente no container, rode:

```sh
pytest


### Detalhe de um pokémon
GET /pokemons/1

Exemplo de resposta:
```json
{
  "name": "bulbasaur",
  "id": 1,
  "height": 7,
  "weight": 69,
  "types": ["grass", "poison"],
  "sprites": {
    "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
    "...": "..."
  }
}
