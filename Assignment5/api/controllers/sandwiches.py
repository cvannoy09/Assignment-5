from fastapi import HTTPException
from sqlalchemy.orm import Session
from api.models import models
from api.models import schemas


def create(db: Session, sandwich: schemas.SandwichCreate):
    db_sandwich = api.models.Sandwich(**sandwich.dict())
    db.add(db_sandwich)
    db.commit()
    db.refresh(db_sandwich)
    return db_sandwich


def read_all(db: Session):
    return db.query(api.models.Sandwich).all()


def read_one(db: Session, sandwich_id: int):
    return db.query(api.models.Sandwich).filter(api.models.Sandwich.id == sandwich_id).first()


def update(db: Session, sandwich_id: int, sandwich: schemas.SandwichUpdate):
    db_sandwich = db.query(api.models.Sandwich).filter(api.models.Sandwich.id == sandwich_id)
    if not db_sandwich.first():
        raise HTTPException(status_code=404, detail="Sandwich not found")

    update_data = sandwich.dict(exclude_unset=True)
    db_sandwich.update(update_data, synchronize_session=False)
    db.commit()
    return db_sandwich.first()


def delete(db: Session, sandwich_id: int):
    db_sandwich = db.query(api.models.Sandwich).filter(api.models.Sandwich.id == sandwich_id)
    if not db_sandwich.first():
        raise HTTPException(status_code=404, detail="Sandwich not found")

    db_sandwich.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Sandwich deleted successfully"}