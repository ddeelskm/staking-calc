from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None


class PoolBase(BaseModel):
    name: str
    apr: float = Field(ge=0)
    description: Optional[str] = None


class PoolCreate(PoolBase):
    pass


class PoolUpdate(BaseModel):
    name: Optional[str] = None
    apr: Optional[float] = Field(None, ge=0)
    description: Optional[str] = None


class PoolOut(PoolBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class StakeBase(BaseModel):
    pool_id: int
    amount: float = Field(gt=0)


class StakeCreate(StakeBase):
    pass


class StakeOut(StakeBase):
    id: int
    user_id: int
    start_date: datetime
    rewards: List['RewardOut'] = []

    class Config:
        from_attributes = True


class RewardHistoryBase(BaseModel):
    reward_amount: float


class RewardCreate(RewardHistoryBase):
    stake_id: int


class RewardOut(RewardHistoryBase):
    id: int
    stake_id: int
    timestamp: datetime

    class Config:
        from_attributes = True


class RewardCalculate(BaseModel):
    stake_id: int
    end_date: datetime


class RewardCalculated(BaseModel):
    stake_id: int
    reward_amount: float

    class Config:
        from_attributes = True


StakeOut.update_forward_refs()
