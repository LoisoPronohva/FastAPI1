from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional, List
from app import crud, schemas, auth
from app.database import get_db
from app.auth import get_current_user, check_user_permission

router = APIRouter(prefix="/advertisement", tags=["advertisements"])


@router.post("/", response_model=schemas.Advertisement, status_code=status.HTTP_201_CREATED)
def create_advertisement(
        advertisement: schemas.AdvertisementCreate,
        current_user: Optional[schemas.UserInDB] = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authentication required to create advertisements"
        )

    #Проверка роли
    if current_user.role not in [schemas.UserRole.USER, schemas.UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to create advertisements"
        )

    return crud.create_advertisement(
        db=db,
        advertisement=advertisement,
        owner_id=current_user.id
    )


@router.get("/{advertisement_id}", response_model=schemas.Advertisement)
def read_advertisement(
        advertisement_id: int,
        db: Session = Depends(get_db)
):
    db_advertisement = crud.get_advertisement(db, advertisement_id=advertisement_id)
    if db_advertisement is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return db_advertisement


@router.patch("/{advertisement_id}", response_model=schemas.Advertisement)
def update_advertisement(
        advertisement_id: int,
        advertisement_update: schemas.AdvertisementUpdate,
        current_user: schemas.UserInDB = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    db_advertisement = crud.get_advertisement(db, advertisement_id=advertisement_id)
    if db_advertisement is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")

    #Проверка прав
    if current_user.role != schemas.UserRole.ADMIN:
        if db_advertisement.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot update other user's advertisement"
            )

    updated_advertisement = crud.update_advertisement(
        db=db,
        advertisement_id=advertisement_id,
        advertisement_update=advertisement_update
    )

    return updated_advertisement


@router.delete("/{advertisement_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_advertisement(
        advertisement_id: int,
        current_user: schemas.UserInDB = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    db_advertisement = crud.get_advertisement(db, advertisement_id=advertisement_id)
    if db_advertisement is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")

    # Проверка прав:
    if current_user.role != schemas.UserRole.ADMIN:
        if db_advertisement.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot delete other user's advertisement"
            )

    success = crud.delete_advertisement(db=db, advertisement_id=advertisement_id)
    if not success:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return None


@router.get("/", response_model=List[schemas.Advertisement])
def search_advertisements(
        title: Optional[str] = Query(None, description="Search in title"),
        author: Optional[str] = Query(None, description="Search by author"),
        description: Optional[str] = Query(None, description="Search in description"),
        min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
        max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
        search_text: Optional[str] = Query(None, description="Search in title, description or author"),
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        sort_by: str = Query("created_at", description="Sort field (title, price, created_at, author)"),
        sort_order: str = Query("desc", description="Sort order (asc or desc)"),
        db: Session = Depends(get_db)
):
    valid_sort_fields = ["title", "price", "created_at", "author"]
    if sort_by not in valid_sort_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort field. Must be one of: {valid_sort_fields}"
        )

    if sort_order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort order. Must be 'asc' or 'desc'"
        )

    return crud.search_advertisements(
        db=db,
        title=title,
        author=author,
        description=description,
        min_price=min_price,
        max_price=max_price,
        search_text=search_text,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order
    )