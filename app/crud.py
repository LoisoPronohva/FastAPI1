from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc
from typing import Optional
from app import models, schemas
from app.auth import get_password_hash, verify_password


# User CRUD
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=models.UserRole.USER
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = get_user_by_id(db, user_id)
    if db_user:
        update_data = user_update.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

        for key, value in update_data.items():
            setattr(db_user, key, value)

        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user_by_id(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_advertisement(db: Session, advertisement: schemas.AdvertisementCreate, owner_id: Optional[int] = None):
    db_advertisement = models.Advertisement(**advertisement.model_dump())
    if owner_id:
        db_advertisement.owner_id = owner_id
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


def search_advertisements(
        db: Session,
        title: Optional[str] = None,
        author: Optional[str] = None,
        description: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        search_text: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "created_at",
        sort_order: str = "desc"
):
    query = db.query(models.Advertisement)

    if title:
        query = query.filter(models.Advertisement.title.ilike(f"%{title}%"))

    if author:
        query = query.filter(models.Advertisement.author.ilike(f"%{author}%"))

    if description:
        query = query.filter(models.Advertisement.description.ilike(f"%{description}%"))

    if min_price is not None:
        query = query.filter(models.Advertisement.price >= min_price)

    if max_price is not None:
        query = query.filter(models.Advertisement.price <= max_price)

    if search_text:
        query = query.filter(
            or_(
                models.Advertisement.title.ilike(f"%{search_text}%"),
                models.Advertisement.description.ilike(f"%{search_text}%"),
                models.Advertisement.author.ilike(f"%{search_text}%")
            )
        )

    # Сортировка
    sort_column = getattr(models.Advertisement, sort_by, models.Advertisement.created_at)
    if sort_order.lower() == "asc":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))

    return query.offset(skip).limit(limit).all()


def get_advertisements(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Advertisement).offset(skip).limit(limit).all()