import httpx
from fastapi import FastAPI, Query, HTTPException

app = FastAPI()

POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon"

@app.get("/pokemons")
async def list_pokemons(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{POKEAPI_URL}?limit={limit}&offset={offset}")
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Erro ao acessar a PokéAPI")
        data = response.json()
    
    pagination = {
        "total": data["count"],
        "limit": limit,
        "offset": offset,
        "next": f"/pokemons?limit={limit}&offset={offset+limit}" if data["next"] else None,
        "previous": f"/pokemons?limit={limit}&offset={offset-limit}" if data["previous"] and offset-limit >= 0 else None
    }
    return {
        "data": data["results"],
        "pagination": pagination
    }

@app.get("/pokemons/{pokemon_id}")
async def get_pokemon(pokemon_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{POKEAPI_URL}/{pokemon_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Pokémon não encontrado")
        elif response.status_code != 200:
            raise HTTPException(status_code=502, detail="Erro ao acessar a PokéAPI")
        data = response.json()
        return {
            "name": data["name"],
            "id": data["id"],
            "height": data["height"],
            "weight": data["weight"],
            "types": [t["type"]["name"] for t in data["types"]],
            "sprites": data["sprites"],
        }