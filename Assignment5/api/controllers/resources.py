from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from api.dependencies.database import get_db
from api.models import models
from api.models import schemas

# Create
def create(db: Session, resource: schemas.ResourceCreate):
    db_resource = models.Resource(**resource.dict())
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

# Read All
def read_all(db: Session):
    return db.query(models.Resource).all()

# Read One
def read_one(db: Session, resource_id: int):
    return db.query(models.Resource).filter(models.Resource.id == resource_id).first()

# Update
def update(db: Session, resource_id: int, resource: schemas.ResourceUpdate):
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id)
    if not db_resource.first():
        raise HTTPException(status_code=404, detail="Resource not found")
    db_resource.update(resource.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return db_resource.first()

# Delete
def delete(db: Session, resource_id: int):
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id)
    if not db_resource.first():
        raise HTTPException(status_code=404, detail="Resource not found")
    db_resource.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Resource deleted successfully"}