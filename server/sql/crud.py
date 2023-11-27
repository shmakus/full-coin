from sqlalchemy.orm import Session
from . import schemas
from database import models
from .schemas import *


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_exchange(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.coolcoin).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_give_pair_name(db: Session):
    return db.query(models.CurrencyRate.give_pair_name).distinct().all()


def get_receive_pair_name(db: Session):
    return db.query(models.CurrencyRate.receive_pair_name).distinct().all()


def create_exchange(db: Session, exchange: ExchangeCreate):
    db_exchange = models.Exchanges(**exchange.dict())
    db.add(db_exchange)
    db.commit()
    db.refresh(db_exchange)
    return db_exchange


def get_currency_pairs(db: Session) -> dict:
    give_pair_name = db.query(models.CurrencyRate.give_pair_name).distinct().all()
    receive_pair_name = db.query(models.CurrencyRate.receive_pair_name).distinct().all()

    give_pair_name = [pair[0] for pair in give_pair_name]
    receive_pair_name = [pair[0] for pair in receive_pair_name]

    return {"give_pair_name": give_pair_name, "receive_pair_name": receive_pair_name}