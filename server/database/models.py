from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship

from database.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)

    # Определение отношения с Review
    reviews = relationship("Review", back_populates="user")


class CurrencyRate(Base):
    __tablename__ = "Courses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    give_count = Column(String, index=True) #отдаю 1
    give_name_coin = Column(String) #отдаю USDT
    give_pair_name = Column(String) #отдаю Techer
    receive_count = Column(String) #получаю 1000
    receive_name_coin = Column(String) #получаю RUB
    receive_pair_name = Column(String) #получаю Наличные RUB
    reserve_count = Column(String) #резерв
    reserve_name_coin = Column(String) #резерв
    link = Column(String) #ссылка
    trading_pair = Column(String) #USDT_RUB
    exchange_id = Column(Integer) #fee
    exchange_name = Column(String)


class Exchange(Base):
    __tablename__ = "exchanges"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    exchange_name = Column(String, unique=True)
    descriptions = Column(String)
    link = Column(String, unique=True)

    # Определение отношения с Review
    reviews = relationship("Review", back_populates="exchange")

    def calculate_rating(self):
        total_reviews = len(self.reviews)

        if total_reviews == 0:
            return 0.0  # Если отзывов нет, рейтинг 0

        # Считаем количество положительных отзывов
        positive_reviews = sum(1 for review in self.reviews if review.rating == 1)

        # Считаем количество отрицательных отзывов
        negative_reviews = sum(1 for review in self.reviews if review.rating == -1)

        # Рассчитываем рейтинг
        rating = (positive_reviews - negative_reviews) / total_reviews
        return rating


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    exchange_id = Column(Integer, ForeignKey('exchanges.id'))
    comment = Column(String)
    is_positive = Column(Boolean)

    # Определение отношений с User и Exchange
    user = relationship("User", back_populates="reviews")
    exchange = relationship("Exchange", back_populates="reviews")




