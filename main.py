import httpx
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from models import Base, Pokemon
from database import engine, SessionLocal
from pydantic import BaseModel
from typing import List

app = FastAPI()

class PokemonCreate(BaseModel):
    name: str
    height: int
    weight: int
    types: List[str]
    sprites: str

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon"

@app.get("/pokemons")
def get_pokemons(limit: int = Query(20), offset: int = Query(0)):
    
    url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset}"
    r = httpx.get(url)
    if r.status_code != 200:
        return {"detail": "Erro ao consultar PokéAPI."}, 503
    data = r.json()

    pokemons = []
    for item in data["results"]:
        poke_r = httpx.get(item["url"])
        if poke_r.status_code != 200:
            continue
        p = poke_r.json()
        pokemons.append({
            "id": p["id"],
            "name": p["name"],
            "height": p["height"],
            "weight": p["weight"],
            "types": [t["type"]["name"] for t in p["types"]],
            "sprites": p["sprites"]
            })

    return {
        "data": pokemons,
        "pagination": {
            "count": data["count"],
            "limit": limit,
            "offset": offset,
        },
    }


@app.get("/pokemons/{poke_id}")
def get_pokemon(poke_id: int):

    url = f"https://pokeapi.co/api/v2/pokemon/{poke_id}"
    r = httpx.get(url)
    if r.status_code != 200:
        raise HTTPException(status_code=404, detail="Pokémon não encontrado")
    p = r.json()
    return {
        "id": p["id"],
        "name": p["name"],
        "height": p["height"],
        "weight": p["weight"],
        "types": [t["type"]["name"] for t in p["types"]],
        "sprites": p["sprites"]
    }

@app.post("/pokemons/local", response_model=dict)
def create_local_pokemon(pokemon: PokemonCreate, db: Session = Depends(get_db)):
    if db.query(Pokemon).filter(Pokemon.name == pokemon.name).first():
        raise HTTPException(status_code=400, detail="Pokémon com esse nome já existe.")
    pokemon_obj = Pokemon(**pokemon.model_dump())
    db.add(pokemon_obj)
    db.commit()
    db.refresh(pokemon_obj)
    return {
        "id": pokemon_obj.id,
        "name": pokemon_obj.name,
        "height": pokemon_obj.height,
        "weight": pokemon_obj.weight,
        "types": pokemon_obj.types,
        "sprites": pokemon_obj.sprites,
    }

@app.post("/pokemons", response_model=dict)
def create_pokemon(pokemon: PokemonCreate, db: Session = Depends(get_db)):
    if db.query(Pokemon).filter(Pokemon.name == pokemon["name"]).first():
        raise HTTPException(status_code=400, detail="Pokemon com esse nome já existe.")
    pokemon = Pokemon(**pokemon)
    db.add(pokemon)
    db.commit()
    db.refresh(pokemon)
    return {
        "id": pokemon.id,
        "name": pokemon.name,
        "height": pokemon.height,
        "weight": pokemon.weight,
        "types": pokemon.types,
        "sprites": pokemon.sprites,
    }

@app.get("/pokemons/local/{id_or_name}", response_model=dict)
def get_local_pokemon(id_or_name: str, db: Session = Depends(get_db)):
    query = None
    if id_or_name.isdigit():
        query = db.query(Pokemon).filter(Pokemon.id == int(id_or_name)).first()
    else:
        query = db.query(Pokemon).filter(Pokemon.name == id_or_name).first()
    if not query:
        raise HTTPException(status_code=404, detail="Pokémon não encontrado.")
    return {
        "id": query.id,
        "name": query.name,
        "height": query.height,
        "weight": query.weight,
        "types": query.types,
        "sprites": query.sprites,
    }

@app.put("/pokemons/local/{id_or_name}", response_model=dict)
def update_pokemon(id_or_name: str, updated: PokemonCreate, db: Session = Depends(get_db)):
    if id_or_name.isdigit():
        pokemon = db.query(Pokemon).filter(Pokemon.id == int(id_or_name)).first()
    else:
        pokemon = db.query(Pokemon).filter(Pokemon.name == id_or_name).first()
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokémon não encontrado.")
    update_data = updated.model_dump()
    for key, value in update_data.items():
        setattr(pokemon, key, value)

    db.commit()
    db.refresh(pokemon)
    return {
        "id": pokemon.id,
        "name": pokemon.name,
        "height": pokemon.height,
        "weight": pokemon.weight,
        "types": pokemon.types,
        "sprites": pokemon.sprites,
    }

@app.delete("/pokemons/local/{id_or_name}", response_model=dict)
def delete_pokemon(id_or_name: str, db: Session = Depends(get_db)):
    if id_or_name.isdigit():
        pokemon = db.query(Pokemon).filter(Pokemon.id == int(id_or_name)).first()
    else:
        pokemon = db.query(Pokemon).filter(Pokemon.name == id_or_name).first()
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokémon não encontrado.")

    db.delete(pokemon)
    db.commit()
    return {"detail": "Pokémon deletado com sucesso."}
