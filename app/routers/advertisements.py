from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional, List
from app import crud, schemas, database

router = APIRouter(prefix="/advertisement", tags=["advertisements"])


@router.post("/", response_model=schemas.Advertisement, status_code=status.HTTP_201_CREATED)
def create_advertisement(
        advertisement: schemas.AdvertisementCreate,
        db: Session = Depends(database.get_db)
):
    return crud.create_advertisement(db=db, advertisement=advertisement)


@router.get("/{advertisement_id}", response_model=schemas.Advertisement)
def read_advertisement(
        advertisement_id: int,
        db: Session = Depends(database.get_db)
):
    db_advertisement = crud.get_advertisement(db, advertisement_id=advertisement_id)
    if db_advertisement is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return db_advertisement


@router.patch("/{advertisement_id}", response_model=schemas.Advertisement)
def update_advertisement(
        advertisement_id: int,
        advertisement_update: schemas.AdvertisementUpdate,
        db: Session = Depends(database.get_db)
):
    db_advertisement = crud.update_advertisement(
        db=db,
        advertisement_id=advertisement_id,
        advertisement_update=advertisement_update
    )
    if db_advertisement is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return db_advertisement


@router.delete("/{advertisement_id}")
def delete_advertisement(
        advertisement_id: int,
        db: Session = Depends(database.get_db)
):
    success = crud.delete_advertisement(db=db, advertisement_id=advertisement_id)
    if not success:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return {"message": "Advertisement deleted successfully"}


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
        db: Session = Depends(database.get_db)
):
    search_params = {}
    if title:
        search_params['title'] = title
    if author:
        search_params['author'] = author
    if description:
        search_params['description'] = description
    if min_price is not None:
        search_params['min_price'] = min_price
    if max_price is not None:
        search_params['max_price'] = max_price
    if search_text:
        search_params['search_text'] = search_text

    return crud.search_advertisements(
        db=db,
        search_params=search_params,
        skip=skip,
        limit=limit
    )