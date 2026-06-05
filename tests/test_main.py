import os
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from database import engine
from models import Base

Base.metadata.create_all(bind=engine)

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_pokemons_list():
    response = client.get("/pokemons?limit=5&offset=0")
    assert response.status_code == 200
    assert "data" in response.json()
    assert "pagination" in response.json()

def test_pokemon_detail():
    response = client.get("/pokemons/1")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "id" in data
    assert "height" in data
    assert "types" in data

def test_pokemon_not_found():
    response = client.get("/pokemons/9999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Pokémon não encontrado"

def test_create_local_pokemon():
    payload = {
        "name": "testcreate",
        "height": 10,
        "weight": 100,
        "type": "dark",
        "sprites": "url"
    }
    response = client.post("/pokemons/local", json=payload)
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["name"] == "testcreate"
    assert data["type"] == "dark"

def test_get_local_pokemon():
    payload = {
        "name": "testget",
        "height": 8,
        "weight": 80,
        "type": "water",
        "sprites": "url2"
    }
    resp_create = client.post("/pokemons/local", json=payload)
    assert resp_create.status_code in [200, 201]
    data_create = resp_create.json()
    assert "id" in data_create
    poke_id = data_create["id"]

    resp = client.get(f"/pokemons/local/{poke_id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "testget"

    resp2 = client.get("/pokemons/local/testget")
    assert resp2.status_code == 200
    assert resp2.json()["id"] == poke_id

def test_update_local_pokemon():
    payload = { "name": "testupdate", "height": 6, "weight": 66, "type": "fairy", "sprites": "url3" }
    resp_create = client.post("/pokemons/local", json=payload)
    assert resp_create.status_code in [200, 201]
    data_create = resp_create.json()
    assert "id" in data_create
    poke_id = data_create["id"]

    payload_update = { "name": "testupdate", "height": 12, "weight": 77, "type": "fairy", "sprites": "url4" }
    resp = client.put(f"/pokemons/local/{poke_id}", json=payload_update)
    assert resp.status_code == 200
    data = resp.json()
    assert data["height"] == 12
    assert data["weight"] == 77

def test_delete_local_pokemon():
    payload = { "name": "testdelete", "height": 3, "weight": 30, "type": "ghost", "sprites": "url5" }
    resp_create = client.post("/pokemons/local", json=payload)
    assert resp_create.status_code in [200, 201]
    data_create = resp_create.json()
    assert "id" in data_create
    poke_id = data_create["id"]

    resp = client.delete(f"/pokemons/local/{poke_id}")
    assert resp.status_code == 200
    assert resp.json()["detail"] == "Pokémon deletado com sucesso."

    resp_not_found = client.get(f"/pokemons/local/{poke_id}")
    assert resp_not_found.status_code == 404

def test_update_local_pokemon_not_found():
    payload_update = {
        "name": "naoencontra",
        "height": 1,
        "weight": 1,
        "type": "ghost",
        "sprites": "url"
    }
    resp = client.put("/pokemons/local/999999", json=payload_update)
    assert resp.status_code == 404

def test_delete_local_pokemon_not_found():
    resp = client.delete("/pokemons/local/999999")
    assert resp.status_code == 404
