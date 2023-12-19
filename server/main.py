from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi import FastAPI, Query

from fastapi.middleware.cors import CORSMiddleware

from database.models import *
from sql import crud, schemas
from database import models
from database.base import SessionLocal, engine



from fastapi.responses import JSONResponse
from database.base import SessionLocal
from database.models import CurrencyRate

from pydantic import BaseModel
from typing import List

from sql.schemas import *

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Настройка CORS для разрешения запросов с вашего фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Замените на адрес вашего фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


# Создаем API-маршрут для получения всех курсов для определенного обменника
@app.get("/exchange/{exchange_id}/currencies")
async def get_currencies_for_exchange(exchange_id: int):
    db = SessionLocal()
    currencies = db.query(CurrencyRate).filter_by(exchange_id=exchange_id).all()
    db.close()
    return currencies


# Создаем API-маршрут для вывода конкретного обменни
@app.get("/exchange/{id}")
async def get_exchange(id: int):
    db = SessionLocal()
    exchang = db.query(Exchanges).filter_by(id=id).all()
    db.close()
    return exchang


# Создаем API-маршрут для вывода всех курсов
@app.get("/courses")
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(CurrencyRate).all()
    return courses


@app.get("/exchanges")
async def get_exchange():
    db = SessionLocal()
    exchanges = db.query(Exchange).all()
    db.close()
    return exchanges


@app.post("/filter", response_model=List[CurrencyRateResponse])
def filter_currency_rates(filter_params: FilterParams):
    get_give_pair_name = filter_params.get_give_pair_name
    receive_pair_name = filter_params.receive_pair_name

    with SessionLocal() as db:
        currency_rates = db.query(CurrencyRate).filter_by(get_give_pair_name=get_give_pair_name, receive_pair_name=receive_pair_name).all()

    if not currency_rates:
        raise HTTPException(status_code=404, detail="Курсы не найдены")

    return currency_rates


@app.get("/pair_names/")
async def get_pair_names(db: Session = Depends(get_db)):
    receive_pair_name = crud.get_give_pair_name(db)
    return receive_pair_name


@app.get("/payment_method/")
async def get_payment_method(db: Session = Depends(get_db)):
    pair_names = crud.get_receive_pair_name(db)
    return pair_names


@app.post("/create_exchange/", response_model=schemas.ExchangeCreate)
def create_exchange(exchange: schemas.ExchangeCreate):
    db = SessionLocal()
    db_exchange = crud.create_exchange(db, exchange)
    db.close()
    return db_exchange


def get_currency_rates(
    db: Session,
    give_pair_name: str = None,
    receive_pair_name: str = None,
    limit: int = 10
) -> List[CurrencyRate]:
    query = db.query(CurrencyRate)

    if give_pair_name:
        query = query.filter(CurrencyRate.give_pair_name == give_pair_name)

    if receive_pair_name:
        query = query.filter(CurrencyRate.receive_pair_name == receive_pair_name)

    return query.limit(limit).all()


@app.get("/currency-rates/")
async def get_currency_rates_endpoint(
    give_pair_name: str = Query(None, description="The currency you want to give"),
    receive_pair_name: str = Query(None, description="The payment method you want to use"),
    limit: int = Query(10, description="Limit the number of results"),
):
    try:
        with SessionLocal() as db:
            rates = get_currency_rates(db, give_pair_name, receive_pair_name, limit)
            result = [
                {
                    "id": rate.id,
                    "exchange_name": rate.exchange_name,
                    "give_count": float(rate.give_count),
                    "give_name_coin": rate.give_name_coin,
                    "give_pair_name": rate.give_pair_name,
                    "receive_count": float(rate.receive_count),
                    "receive_name_coin": rate.receive_name_coin,
                    "receive_pair_name": rate.receive_pair_name,
                    "reserve_count": rate.reserve_count,
                    "reserve_name_coin": rate.reserve_name_coin,
                    "link": rate.link,
                    "trading_pair": rate.trading_pair,
                    "exchange_id": rate.exchange_id,
                }
                for rate in rates
            ]
            return JSONResponse(content=result)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JSONResponse(
            content={"error": f"An error occurred: {str(e)}"}, status_code=500
        )

# Новый маршрут для получения списка уникальных валютных пар
@app.get("/currency-pairs", response_model=dict)
def get_currency_pairs(db: Session = Depends(get_db)):
    return crud.get_currency_pairs(db)


