from passlib.context import CryptContext
from sqlalchemy.orm import Session

import models
import schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_pool(db: Session, pool_id: int):
    return db.query(models.StakingPool).filter(models.StakingPool.id == pool_id).first()


def get_pools(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.StakingPool).offset(skip).limit(limit).all()


def create_pool(db: Session, pool: schemas.PoolCreate):
    db_pool = models.StakingPool(
        name=pool.name,
        apr=pool.apr,
        description=pool.description
    )
    db.add(db_pool)
    db.commit()
    db.refresh(db_pool)
    return db_pool


def update_pool(db: Session, pool_id: int, pool_update: schemas.PoolUpdate):
    db_pool = get_pool(db, pool_id)
    if not db_pool:
        return None
    update_data = pool_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_pool, field, value)
    db.commit()
    db.refresh(db_pool)
    return db_pool


def delete_pool(db: Session, pool_id: int):
    db_pool = get_pool(db, pool_id)
    if db_pool:
        db.delete(db_pool)
        db.commit()
    return db_pool


def get_stakes_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Stake).filter(models.Stake.user_id == user_id).offset(skip).limit(limit).all()


def get_stake(db: Session, stake_id: int):
    return db.query(models.Stake).filter(models.Stake.id == stake_id).first()


def create_stake(db: Session, stake: schemas.StakeCreate, user_id: int):
    db_stake = models.Stake(
        user_id=user_id,
        pool_id=stake.pool_id,
        amount=stake.amount
    )
    db.add(db_stake)
    db.commit()
    db.refresh(db_stake)
    return db_stake


def get_rewards_by_stake(db: Session, stake_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.RewardHistory).filter(models.RewardHistory.stake_id == stake_id).offset(skip).limit(
        limit).all()


def create_reward(db: Session, reward: schemas.RewardCreate):
    db_reward = models.RewardHistory(
        stake_id=reward.stake_id,
        reward_amount=reward.reward_amount
    )
    db.add(db_reward)
    db.commit()
    db.refresh(db_reward)
    return db_reward
