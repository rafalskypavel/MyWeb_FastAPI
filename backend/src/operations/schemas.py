import enum
from pydantic import BaseModel, Field


class CurrencyEnum(str, enum.Enum):
    RUB = "RUB"
    BYN = "BYN"
    USD = "USD"
    EUR = "EUR"


class AvailabilityEnum(str, enum.Enum):
    IN_STOCK = "in_stock"
    OUT_OF_STOCK = "out_of_stock"
    COMING_SOON = "coming_soon"


class ProductCreate(BaseModel):
    id: int = Field(..., title="Product ID")
    name: str = Field(..., title="Product Name")
    brand: str = Field(..., title="Product Brand")
    description: str = Field(None, title="Product Description")
    price: float = Field(..., title="Product Price")
    old_price: float = Field(None, title="Old Price", description="Previous price if applicable")
    currency: CurrencyEnum = Field(..., title="Currency", description="Currency code")
    availability: AvailabilityEnum = Field(..., title="Availability", description="Product availability status")
    images: dict = Field(..., title="Images", description="Product images as JSON")


class ProductUpdate(ProductCreate):
    id: int = Field(..., title="Product ID", description="Product ID to update")
