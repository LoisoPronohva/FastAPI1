from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app import crud, schemas, auth
from app.database import get_db
from app.auth import get_current_user, check_user_permission

router = APIRouter(prefix="/user", tags=["users"])


@router.post("/", response_model=schemas.UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(
        user: schemas.UserCreate,
        db: Session = Depends(get_db)
):
    #Проверка имени
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )

    #Создаем
    return crud.create_user(db=db, user=user)


@router.get("/", response_model=schemas.UserPublic)
def get_current_user_info(
        current_user: schemas.UserInDB = Depends(get_current_user)
):
    return current_user


@router.get("/{user_id}", response_model=schemas.UserPublic)
def get_user(
        user_id: int,
        current_user: Optional[schemas.UserInDB] = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if current_user:
        if current_user.id == user_id or current_user.role == schemas.UserRole.ADMIN:
            return db_user

    response = schemas.UserPublic.model_validate(db_user)
    response.email = None
    return response


@router.patch("/{user_id}", response_model=schemas.UserPublic)
def update_user(
        user_id: int,
        user_update: schemas.UserUpdate,
        current_user: schemas.UserInDB = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    #Проверка прав
    check_user_permission(current_user, user_id=user_id)

    db_user = crud.update_user(db=db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
        user_id: int,
        current_user: schemas.UserInDB = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    #Проверка прав
    check_user_permission(current_user, user_id=user_id)

    success = crud.delete_user(db=db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return None