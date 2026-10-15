"""FastAPI application entrypoint and REST API routes."""

from fastapi import FastAPI, HTTPException, status

from app.models import product_store
from app.schemas import (
    HealthResponse,
    ProductCreate,
    ProductResponse,
    ProductUpdate,
    WelcomeResponse,
)

app = FastAPI(
    title="Product Management API",
    description=(
        "Production-minded REST API demonstrating FastAPI, Pydantic validation, "
        "Docker containerization, and GitHub Actions CI/CD pipeline automation."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get(
    "/",
    response_model=WelcomeResponse,
    status_code=status.HTTP_200_OK,
    summary="Root welcome endpoint",
    tags=["General"],
)
def get_root() -> WelcomeResponse:
    """Return a welcome message with API info and Swagger documentation link."""
    return WelcomeResponse(
        message="Welcome to the Product Management API",
        docs_url="/docs",
        version="1.0.0",
    )


@app.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check endpoint",
    tags=["Monitoring"],
)
def get_health() -> HealthResponse:
    """Perform a service health check to confirm the API server is operational."""
    return HealthResponse(status="healthy", service="product-api")


@app.post(
    "/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product",
    tags=["Products"],
)
def create_product(payload: ProductCreate) -> ProductResponse:
    """Validate request payload and create a new product in the catalog."""
    product = product_store.create(
        name=payload.name,
        description=payload.description,
        price=payload.price,
        in_stock=payload.in_stock,
    )
    return ProductResponse.model_validate(product)


@app.get(
    "/products",
    response_model=list[ProductResponse],
    status_code=status.HTTP_200_OK,
    summary="List all products",
    tags=["Products"],
)
def list_products() -> list[ProductResponse]:
    """Retrieve all products currently stored in the catalog."""
    products = product_store.get_all()
    return [ProductResponse.model_validate(p) for p in products]


@app.get(
    "/products/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a single product by ID",
    tags=["Products"],
)
def get_product(product_id: int) -> ProductResponse:
    """Retrieve details of a single product using its numeric identifier."""
    product = product_store.get_by_id(product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found",
        )
    return ProductResponse.model_validate(product)


@app.put(
    "/products/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
    summary="Update an existing product",
    tags=["Products"],
)
def update_product(product_id: int, payload: ProductUpdate) -> ProductResponse:
    """Update fields of an existing product. Returns 404 if product does not exist."""
    existing = product_store.get_by_id(product_id)
    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found",
        )

    updated = product_store.update(
        product_id=product_id,
        name=payload.name,
        description=payload.description,
        price=payload.price,
        in_stock=payload.in_stock,
    )
    return ProductResponse.model_validate(updated)


@app.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a product by ID",
    tags=["Products"],
)
def delete_product(product_id: int) -> None:
    """Delete a product from the catalog. Returns 404 if product does not exist."""
    deleted = product_store.delete(product_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found",
        )
    return None
