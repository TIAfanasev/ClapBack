from sqlalchemy import ARRAY, Boolean, Column, DateTime, \
    Float, ForeignKey, func, Integer, Table, Text, String
from sqlalchemy.orm import DeclarativeBase

from .db import metadata


class Base(DeclarativeBase):
    pass

clients = Table(
    "clients",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("fio", String),
    Column("phone", String, unique=True),
    Column("email", String, unique=True),
    Column("password", String),
    Column("telegram", String, nullable=True),
)

buildings = Table(
    "buildings",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("address", String),
    Column("square", String),
    Column("price", Float),
    Column("descript", Text),
    Column("buildings_used", ARRAY(Integer), server_default="{}")
)

apps = Table(
    "apps",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("client", Integer, ForeignKey("clients.id")),
    Column("building", Integer, ForeignKey("buildings.id")),
    Column("date", DateTime, server_default=func.now()),
    Column("ready", Boolean),
    Column("used", Boolean)
)

class Clients(Base):
    __table__ = clients


class Buildings(Base):
    __table__ = buildings


class Apps(Base):
    __table__ = apps
