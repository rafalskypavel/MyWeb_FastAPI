from sqlalchemy import Table, Column, Integer, String, Enum, JSON, Float
from sqlalchemy.dialects.postgresql import JSONB

from .schemas import CurrencyEnum, AvailabilityEnum

from database import metadata

product = Table(
    "product",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("brand", String, nullable=False),
    Column("description", String, nullable=True),
    Column("price", Float, nullable=False),
    Column("old_price", Float, nullable=True),
    Column("currency", Enum(CurrencyEnum), nullable=False),
    Column("availability", Enum(AvailabilityEnum), nullable=False),
    Column("images", JSONB),  # Используем JSONB для хранения JSON-подобных данных
)
