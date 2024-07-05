from sqlalchemy.orm import Session

import schemas
from models import models


def get_sim(db: Session, sim_id: int):
    return db.query(models.Sim).filter(models.Sim.id == sim_id).first()


def get_sims(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sim).offset(skip).limit(limit).all()


def create_sim(db: Session, sim: schemas.SimCreate):
    db_sim = models.Sim(**sim.model_dump())
    db.add(db_sim)
    db.commit()
    db.refresh(db_sim)
    return db_sim

