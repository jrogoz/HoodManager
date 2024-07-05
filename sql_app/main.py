from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, schemas
from .models import models
from .database import SessionLocal, engine


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/sims/", response_model=schemas.Sim)
def create_sim(sim: schemas.SimCreate, db: Session = Depends(get_db)):
    return crud.create_sim(db, sim=sim)


@app.get('/sims/{sim_id}', response_model=schemas.Sim)
def read_sim(sim_id: int, db: Session = Depends(get_db)):
    db_sim = crud.get_sim(db,sim_id=sim_id)
    if db_sim is None:
        raise HTTPException(status_code=404, detail='Sim not found')
    return db_sim


@app.get('/sims/', response_model=list[schemas.Sim])
def read_sims(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_sims(db, skip=skip, limit=limit)
