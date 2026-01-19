from sqlalchemy.orm import Session
from sqlalchemy import or_
from app import models, schemas


def create_advertisement(db: Session, advertisement: schemas.AdvertisementCreate):
    db_advertisement = models.Advertisement(**advertisement.model_dump())
    db.add(db_advertisement)
    db.commit()
    db.refresh(db_advertisement)
    return db_advertisement


def get_advertisement(db: Session, advertisement_id: int):
    return db.query(models.Advertisement).filter(models.Advertisement.id == advertisement_id).first()


def update_advertisement(db: Session, advertisement_id: int, advertisement_update: schemas.AdvertisementUpdate):
    db_advertisement = get_advertisement(db, advertisement_id)
    if db_advertisement:
        update_data = advertisement_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_advertisement, key, value)
        db.commit()
        db.refresh(db_advertisement)
    return db_advertisement


def delete_advertisement(db: Session, advertisement_id: int):
    db_advertisement = get_advertisement(db, advertisement_id)
    if db_advertisement:
        db.delete(db_advertisement)
        db.commit()
        return True
    return False


def search_advertisements(db: Session, search_params: dict, skip: int = 0, limit: int = 100):
    query = db.query(models.Advertisement)

    if 'title' in search_params:
        query = query.filter(models.Advertisement.title.ilike(f"%{search_params['title']}%"))

    if 'author' in search_params:
        query = query.filter(models.Advertisement.author.ilike(f"%{search_params['author']}%"))

    if 'min_price' in search_params:
        query = query.filter(models.Advertisement.price >= search_params['min_price'])

    if 'max_price' in search_params:
        query = query.filter(models.Advertisement.price <= search_params['max_price'])

    if 'description' in search_params:
        query = query.filter(models.Advertisement.description.ilike(f"%{search_params['description']}%"))

    if 'search_text' in search_params:
        search_text = search_params['search_text']
        query = query.filter(
            or_(
                models.Advertisement.title.ilike(f"%{search_text}%"),
                models.Advertisement.description.ilike(f"%{search_text}%"),
                models.Advertisement.author.ilike(f"%{search_text}%")
            )
        )

    return query.offset(skip).limit(limit).all()


def get_advertisements(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Advertisement).offset(skip).limit(limit).all()