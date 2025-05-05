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
    tags=["Вознаграждения"],
)


@router.get("/rewards/{stake_id}", response_model=List[schemas.RewardOut])
def read_rewards(
        stake_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    stake = crud.get_stake(db, stake_id)
    if not stake or stake.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ставка не найдена"
        )
    return crud.get_rewards_by_stake(db, stake_id)


@router.post("/rewards/calculate", response_model=schemas.RewardCalculated)
def calculate_reward(
        request: schemas.RewardCalculate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    stake = crud.get_stake(db, request.stake_id)
    if not stake or stake.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ставка не найдена"
        )
    if request.end_date < stake.start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Дата конца раньше даты начала ставки"
        )
    pool = crud.get_pool(db, stake.pool_id)
    days = (request.end_date - stake.start_date).days
    apr = pool.apr / 100
    reward_amount = stake.amount * ((1 + apr) ** (days / 365) - 1)
    crud.create_reward(db, schemas.RewardCreate(
        stake_id=request.stake_id,
        reward_amount=reward_amount
    ))
    return schemas.RewardCalculated(
        stake_id=request.stake_id,
        reward_amount=reward_amount
    )
