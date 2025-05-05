from datetime import timedelta

import crud
import schemas
from database import engine, SessionLocal
from models import Base

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def main():
    db = SessionLocal()
    try:
        user_in = schemas.UserCreate(email="ivan.petrov@gmail.com", password="OverGoodPassword43")
        user = crud.create_user(db, user_in)
        print(f"Создан пользователь: ID={user.id}, email={user.email}")

        pool_in = schemas.PoolCreate(
            name="Ethereum Staking Pool", apr=4.0,
            description="Стейкинг ETH с доходностью 4% годовых"
        )
        pool = crud.create_pool(db, pool_in)
        print(f"Создан пул: ID={pool.id}, name={pool.name}, apr={pool.apr}")

        stake_in = schemas.StakeCreate(pool_id=pool.id, amount=10.0)
        stake = crud.create_stake(db, stake_in, user.id)
        print(f"Создана ставка: ID={stake.id}, amount={stake.amount}, start={stake.start_date}")

        end_date = stake.start_date + timedelta(days=30)
        reward_amount = stake.amount * ((1 + pool.apr/100) ** (30/365) - 1)
        reward_in = schemas.RewardCreate(stake_id=stake.id, reward_amount=reward_amount)
        reward = crud.create_reward(db, reward_in)
        print(f"Начислено вознаграждение: {reward.reward_amount:.6f} токенов, timestamp={reward.timestamp}")

        rewards = crud.get_rewards_by_stake(db, stake.id)
        print("История вознаграждений:")
        for r in rewards:
            print(f"  ID={r.id}, amount={r.reward_amount:.6f}, at={r.timestamp}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
