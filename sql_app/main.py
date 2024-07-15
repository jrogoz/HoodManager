from fastapi import Depends, FastAPI, HTTPException
import uvicorn
from sqlalchemy.orm import Session

from sql_app import crud, schemas
from sql_app.models import models
from sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def index():
    return {"msg": 'Just working'}

@app.post("/sims/", response_model=schemas.Sim, status_code=201)
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


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_level="debug")