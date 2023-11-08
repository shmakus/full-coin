from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        from_attributes = True


class FilterParams(BaseModel):
    pair_name: str
    payment_method: str


class CurrencyRateResponse(BaseModel):
    id: int
    give: str
    pair_name: str
    receive: str
    payment_method: str
    reserve: str
    link: str
    trading_pair: str
    exchange_id: int


class ExchangeCreate(BaseModel):
    exchange_name: str
    descriptions: str
    link: str
