from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
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
    __tablename__ = "coolcoin"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    give = Column(String)
    pair_name = Column(String)
    receive = Column(String)
    payment_method = Column(String)
    reserve = Column(String)
    link = Column(String)
    trading_pair = Column(String)
    exchange_id = Column(Integer)





class Exchanges(Base):
    __tablename__ = "Exchanges"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True,)
    exchange_name = Column(String, unique=True,)
    descriptions = Column(String)
    link = Column(String, unique=True,)





