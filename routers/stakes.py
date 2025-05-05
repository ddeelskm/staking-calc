from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import get_db
from routers.auth import get_current_user

router = APIRouter(
    prefix="",
    tags=["Ставки"],
)


@router.post("/stakes/", response_model=schemas.StakeOut, status_code=status.HTTP_201_CREATED)
def create_stake(
        stake: schemas.StakeCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    return crud.create_stake(db, stake, current_user.id)


@router.get("/stakes/", response_model=List[schemas.StakeOut])
def read_stakes(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    return crud.get_stakes_by_user(db, current_user.id, skip=skip, limit=limit)


@router.get("/stakes/{stake_id}", response_model=schemas.StakeOut)
def read_stake(
        stake_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    db_stake = crud.get_stake(db, stake_id)
    if not db_stake or db_stake.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ставка не найдена"
        )
    return db_stake
