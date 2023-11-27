from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship

from database.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")


class CurrencyRate(Base):
    __tablename__ = "Courses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    give_count = Column(Numeric, index=True) #отдаю 1
    give_name_coin = Column(String) #отдаю USDT
    give_pair_name = Column(String) #отдаю Techer
    receive_count = Column(Numeric, index=True) #получаю 1000
    receive_name_coin = Column(String) #получаю RUB
    receive_pair_name = Column(String) #получаю Наличные RUB
    reserve = Column(String) #резерв
    link = Column(String) #ссылка
    trading_pair = Column(String) #USDT_RUB
    exchange_id = Column(Integer) #fee
    exchange_name = Column(String)


class Exchanges(Base):
    __tablename__ = "Exchanges"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True,)
    exchange_name = Column(String, unique=True,)
    descriptions = Column(String)
    link = Column(String, unique=True,)





