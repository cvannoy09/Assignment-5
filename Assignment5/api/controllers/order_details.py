from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from api.dependencies.database import get_db
from api.models import models
from api.models import schemas


def create(db: Session, order_detail: schemas.OrderDetailCreate):
    db_order_detail = models.OrderDetail(**order_detail.dict())
    db.add(db_order_detail)
    db.commit()
    db.refresh(db_order_detail)
    return db_order_detail


def read_all(db: Session):
    return db.query(models.OrderDetail).all()


def read_one(db: Session, order_detail_id: int):
    return db.query(models.OrderDetail).filter(models.OrderDetail.id == order_detail_id).first()


def update(db: Session, order_detail_id: int, order_detail: schemas.OrderDetailUpdate):
    db_order_detail = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_detail_id)
    if not db_order_detail.first():
        raise HTTPException(status_code=404, detail="Order detail not found")

    update_data = order_detail.dict(exclude_unset=True)
    db_order_detail.update(update_data, synchronize_session=False)
    db.commit()
    return db_order_detail.first()


def delete(db: Session, order_detail_id: int):
    db_order_detail = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_detail_id)
    if not db_order_detail.first():
        raise HTTPException(status_code=404, detail="Order detail not found")

    db_order_detail.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Order detail deleted"}