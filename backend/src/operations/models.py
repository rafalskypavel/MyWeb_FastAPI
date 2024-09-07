from sqlalchemy import Table, Column, Integer, String, Enum, Float, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from .schemas import CurrencyEnum, AvailabilityEnum

from database import metadata

product = Table(
    "product",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False, unique=True),
    Column("brand", String, nullable=False),
    Column("description", String, nullable=True),
    Column("price", Float, nullable=False),
    Column("old_price", Float, nullable=True),
    Column("currency", Enum(CurrencyEnum), nullable=False),
    Column("availability", Enum(AvailabilityEnum), nullable=False),
    Column("images", JSONB),  # Используем JSONB для хранения JSON-подобных данных
)

product_group = Table(
    "product_group",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False, unique=True),
    Column("parent_id", Integer, ForeignKey("product_group.id")),  # Для подгрупп, ссылается на родительскую группу
)
