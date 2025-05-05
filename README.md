# Калькулятор доходности стейкинга и фарминга
## Основные возможности
### Аутентификация и авторизация

Registrarion: POST /auth/register<br>
Login: POST /auth/login → JWT

### Защищённые роуты через Bearer токен.
### Управление пулами
### CRUD-эндпоинты для пулов:

POST /pools/ — **создать пул**<br>
GET /pools/ — **список пулов**<br>
GET /pools/{id} — **детализация пула**<br>
PUT /pools/{id} — **обновить пул**<br>
DELETE /pools/{id} — **удалить пул**

### Ставки пользователей

POST /stakes/ — **создать ставку (amount, pool_id)**<br>
GET /stakes/ — **получить все ставки текущего пользователя**<br>
GET /stakes/{id} — **детали ставки**

### Расчёт вознаграждений

POST /rewards/calculate — **расчёт и сохранение по формуле сложного процента**<br>
GET /rewards/{stake_id} — **история начислений по ставке**

### Установка и запуск
git clone https://github.com/ваш_логин/staking-calc.git<br>
cd staking-calc<br>
pip install -r requirements.txt<br>
uvicorn main:app --reload

### Документация
**Swagger UI:** http://127.0.0.1:8000/docs<br>
**ReDoc:** http://127.0.0.1:8000/redoc