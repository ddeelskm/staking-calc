from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    stakes = relationship('Stake', back_populates='user')


class StakingPool(Base):
    __tablename__ = 'staking_pools'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    apr = Column(Float, nullable=False, default=0.0)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    stakes = relationship('Stake', back_populates='pool')


class Stake(Base):
    __tablename__ = 'stakes'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    pool_id = Column(Integer, ForeignKey('staking_pools.id'), nullable=False)
    amount = Column(Float, nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='stakes')
    pool = relationship('StakingPool', back_populates='stakes')
    rewards = relationship('RewardHistory', back_populates='stake')


class RewardHistory(Base):
    __tablename__ = 'reward_history'

    id = Column(Integer, primary_key=True, index=True)
    stake_id = Column(Integer, ForeignKey('stakes.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    reward_amount = Column(Float, nullable=False)

    stake = relationship('Stake', back_populates='rewards')
