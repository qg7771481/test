from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI()



class Movie(BaseModel):
    id: int
    title: str
    director: str
    release_year: int
    rating: float

movies_db: List[Movie] = []


@app.get("/movies", response_model=List[Movie])
def get_movies():
    return movies_db


@app.post("/movies", status_code=201)
def add_movie(movie: Movie):

    if any(m.id == movie.id for m in movies_db):
        raise HTTPException(status_code=400, detail="Movie with this ID already exists.")

    current_year = datetime.now().year
    if movie.release_year > current_year:
        raise HTTPException(status_code=400, detail="Release year cannot be in the future.")


    if not (0 <= movie.rating <= 10):
        raise HTTPException(status_code=400, detail="Rating must be between 0 and 10.")

    movies_db.append(movie)
    return {"message": "Movie added successfully"}



@app.get("/movies/{movie_id}", response_model=Movie)
def get_movie(movie_id: int):
    for movie in movies_db:
        if movie.id == movie_id:
            return movie
    raise HTTPException(status_code=404, detail="Movie not found")



@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    for i, movie in enumerate(movies_db):
        if movie.id == movie_id:
            del movies_db[i]
            return {"message": "Movie deleted"}
    raise HTTPException(status_code=404, detail="Movie not found")
