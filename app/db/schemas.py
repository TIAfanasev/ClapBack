import datetime as dt

from pydantic import BaseModel, EmailStr


class ClientsBase(BaseModel):
    fio: str
    phone: str
    email: EmailStr
    telegram: str = ""


class ClientsCreate(ClientsBase):
    password: str


class Clients(ClientsBase):
    id: int
    password: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class Buildings(BaseModel):
    id: int
    address: str
    square: str
    price: float
    descript: str
    buildings_used: list[int] | None = []


class AppsBase(BaseModel):
    client: int
    building: int


class AppsCreate(AppsBase):
    pass


class Apps(AppsBase):
    id: int
    date: dt.datetime = dt.datetime.now()
    ready: bool = False
    used: bool = True
