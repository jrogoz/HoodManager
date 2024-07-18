import datetime

from sqlalchemy.orm import Session

from . import schemas
from .models import models, enums


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


def update_sim(db: Session, sim_id: int, sim_update = schemas.SimBase):
    db_sim = db.query(models.Sim).filter(models.Sim.id == sim_id).first()
    if db_sim:
        for key, value in sim_update.model_dump(exclude_unset=True).items():
            setattr(db_sim, key, value)
        setattr(db_sim, 'last_update', datetime.datetime.now())
        db.commit()
        db.refresh(db_sim)
        return db_sim
    return None


def grow_up_sim(db: Session, sim_id: int):
    db_sim = db.query(models.Sim).filter(models.Sim.id == sim_id).first()
    if db_sim:
        if db_sim.life_stage == enums.LifeStage.ELDER:
            return None
        setattr(db_sim, 'life_stage', db_sim.life_stage.next())
        setattr(db_sim, 'last_update', datetime.datetime.now())
        db.commit()
        db.refresh(db_sim)
        return db_sim
    return None
