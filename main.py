# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import auth, pools, stakes, rewards

app = FastAPI(
    title="Калькулятор доходности стейкинга и фарминга",
    description="API для управления пулами, ставками и расчётом вознаграждений",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(pools.router)
app.include_router(stakes.router)
app.include_router(rewards.router)


@app.get("/", summary="Корневой эндпоинт")
async def root():
    return {"message": "Добро пожаловать в API"}
