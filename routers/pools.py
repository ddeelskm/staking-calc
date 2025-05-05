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
    tags=["Пулы"],
)


@router.post("/pools/", response_model=schemas.PoolOut, status_code=status.HTTP_201_CREATED)
def create_pool(
        pool: schemas.PoolCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    """
    Создание нового пула стейкинга.
    - **pool**: данные нового пула (название, APR, описание)
    - **db**: сессия базы данных
    - **current_user**: авторизованный пользователь
    """
    return crud.create_pool(db, pool)


@router.get("/pools/", response_model=List[schemas.PoolOut])
def read_pools(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    """
    Получение списка пулов стейкинга.
    - **skip**: количество записей для пропуска
    - **limit**: максимальное количество записей в ответе
    - **db**: сессия базы данных
    """
    return crud.get_pools(db, skip=skip, limit=limit)


@router.get("/pools/{pool_id}", response_model=schemas.PoolOut)
def read_pool(
        pool_id: int,
        db: Session = Depends(get_db)
):
    """
    Получение информации о конкретном пуле по его идентификатору.
    - **pool_id**: идентификатор пула
    - **db**: сессия базы данных
    """
    db_pool = crud.get_pool(db, pool_id)
    if not db_pool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пул не найден"
        )
    return db_pool


@router.put("/pools/{pool_id}", response_model=schemas.PoolOut)
def update_pool(
        pool_id: int,
        pool_update: schemas.PoolUpdate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    """
    Обновление данных существующего пула.

    - **pool_id**: идентификатор пула для обновления
    - **pool_update**: новые данные пула (название, APR, описание)
    - **db**: сессия базы данных
    - **current_user**: авторизованный пользователь
    """
    updated = crud.update_pool(db, pool_id, pool_update)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пул не найден"
        )
    return updated


@router.delete("/pools/{pool_id}", response_model=schemas.PoolOut)
def delete_pool(
        pool_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    """
    Удаление пула стейкинга по его идентификатору.
    """
    deleted = crud.delete_pool(db, pool_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пул не найден"
        )
    return deleted