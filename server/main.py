from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database.models import *
from sql import crud, schemas
from database import models
from database.base import SessionLocal, engine

from pydantic import BaseModel
from typing import List

from sql.schemas import *

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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


# Создаем API-маршрут для вывода конкретного обменника
@app.get("/exchange/{id}")
async def get_exchange(id: int):
    db = SessionLocal()
    exchang = db.query(Exchanges).filter_by(id=id).all()
    db.close()
    return exchang


# Создаем API-маршрут для вывода всех оббмеников
@app.get("/exchange/{id}")
async def get_exchange(id: int):
    db = SessionLocal()
    exchange = db.query(Exchanges).filter_by(id=id).all()
    db.close()
    return exchange


@app.get("/exchanges")
async def get_exchange():
    db = SessionLocal()
    exchanges = db.query(Exchanges).all()
    db.close()
    return exchanges


@app.post("/filter", response_model=List[CurrencyRateResponse])
def filter_currency_rates(filter_params: FilterParams):
    pair_name = filter_params.pair_name
    payment_method = filter_params.payment_method

    with SessionLocal() as db:
        currency_rates = db.query(CurrencyRate).filter_by(pair_name=pair_name, payment_method=payment_method).all()

    if not currency_rates:
        raise HTTPException(status_code=404, detail="Курсы не найдены")

    return currency_rates


@app.get("/pair_names/")
async def get_pair_names(db: Session = Depends(get_db)):
    pair_names = crud.get_pair_names(db)
    return pair_names


@app.get("/payment_method/")
async def get_payment_method(db: Session = Depends(get_db)):
    pair_names = crud.get_payment_method(db)
    return pair_names


@app.post("/create_exchange/", response_model=schemas.ExchangeCreate)
def create_exchange(exchange: schemas.ExchangeCreate):
    db = SessionLocal()
    db_exchange = crud.create_exchange(db, exchange)
    db.close()
    return db_exchange
