from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app

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
    