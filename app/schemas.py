"""Pydantic schemas for request validation and response serialization."""

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductBase(BaseModel):
    """Base product attributes shared between schemas."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Name of the product",
        examples=["Ergonomic Mechanical Keyboard"],
    )
    description: str | None = Field(
        default=None,
        max_length=500,
        description="Optional detailed description of the product",
        examples=["Compact wireless keyboard with hot-swappable switches."],
    )
    price: float = Field(
        ...,
        gt=0,
        description="Price in USD (must be strictly greater than 0)",
        examples=[89.99],
    )
    in_stock: bool = Field(
        default=True,
        description="Indicates whether the product is currently in stock",
        examples=[True],
    )

    @field_validator("name")
    @classmethod
    def validate_name_not_blank(cls, value: str) -> str:
        """Ensure product name is not empty or composed solely of whitespace."""
        stripped = value.strip()
        if not stripped:
            raise ValueError("Product name cannot be empty or contain only whitespace.")
        return stripped


class ProductCreate(ProductBase):
    """Payload required to create a new product."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Ergonomic Mechanical Keyboard",
                "description": "Compact wireless keyboard with hot-swappable switches.",
                "price": 89.99,
                "in_stock": True,
            }
        }
    )


class ProductUpdate(BaseModel):
    """Payload to update an existing product. All fields are optional."""

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Updated product name",
        examples=["Ergonomic Mechanical Keyboard v2"],
    )
    description: str | None = Field(
        default=None,
        max_length=500,
        description="Updated description",
        examples=["Upgraded wireless keyboard with RGB lighting."],
    )
    price: float | None = Field(
        default=None,
        gt=0,
        description="Updated price in USD (must be strictly greater than 0)",
        examples=[99.99],
    )
    in_stock: bool | None = Field(
        default=None,
        description="Updated stock availability status",
        examples=[False],
    )

    @field_validator("name")
    @classmethod
    def validate_name_not_blank(cls, value: str | None) -> str | None:
        """Ensure updated name, if provided, is not empty or whitespace."""
        if value is None:
            return value
        stripped = value.strip()
        if not stripped:
            raise ValueError("Product name cannot be empty or contain only whitespace.")
        return stripped

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Ergonomic Mechanical Keyboard v2",
                "price": 99.99,
                "in_stock": False,
            }
        }
    )


class ProductResponse(ProductBase):
    """Product schema returned in API responses, including database ID."""

    id: int = Field(
        ...,
        description="Unique identifier assigned to the product",
        examples=[1],
    )

    model_config = ConfigDict(from_attributes=True)


class HealthResponse(BaseModel):
    """Schema for service health check response."""

    status: str = Field(..., examples=["healthy"])
    service: str = Field(..., examples=["product-api"])


class WelcomeResponse(BaseModel):
    """Schema for root welcome endpoint response."""

    message: str = Field(..., examples=["Welcome to the Product Management API"])
    docs_url: str = Field(..., examples=["/docs"])
    version: str = Field(..., examples=["1.0.0"])
