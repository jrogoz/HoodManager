from sqlalchemy.orm import Session

import schemas
from models import models


def get_sim(db: Session, sim_id: int):
    return db.query(models.Sim).filter(models.Sim.id == sim_id).first()


def get_sims(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sim).offset(skip).limit(limit).all()

