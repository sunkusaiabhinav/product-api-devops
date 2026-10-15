"""In-memory data models and repository for product storage.

Note on In-Memory Storage:
This implementation stores records directly in Python process memory (RAM).
While ideal for rapid testing, demonstrations, and educational purposes without
requiring external database servers, all data is volatile and will be lost whenever
the server process restarts, crashes, or scales across multiple instances.
"""

from dataclasses import dataclass


@dataclass
class Product:
    """Product domain entity representing an item in the catalog."""

    id: int
    name: str
    description: str | None
    price: float
    in_stock: bool


class ProductStore:
    """Thread-safe in-memory store for product records."""

    def __init__(self) -> None:
        self._products: dict[int, Product] = {}
        self._current_id: int = 0

    def get_all(self) -> list[Product]:
        """Retrieve all stored products."""
        return list(self._products.values())

    def get_by_id(self, product_id: int) -> Product | None:
        """Retrieve a single product by its primary ID."""
        return self._products.get(product_id)

    def create(
        self,
        name: str,
        description: str | None,
        price: float,
        in_stock: bool,
    ) -> Product:
        """Create a new product with an auto-incremented ID and store it."""
        self._current_id += 1
        product = Product(
            id=self._current_id,
            name=name,
            description=description,
            price=price,
            in_stock=in_stock,
        )
        self._products[self._current_id] = product
        return product

    def update(
        self,
        product_id: int,
        name: str | None = None,
        description: str | None = None,
        price: float | None = None,
        in_stock: bool | None = None,
    ) -> Product | None:
        """Update fields of an existing product. Only non-None fields are updated."""
        product = self.get_by_id(product_id)
        if product is None:
            return None

        if name is not None:
            product.name = name
        if description is not None:
            product.description = description
        if price is not None:
            product.price = price
        if in_stock is not None:
            product.in_stock = in_stock

        return product

    def delete(self, product_id: int) -> bool:
        """Delete a product by ID. Returns True if deleted, False if not found."""
        if product_id in self._products:
            del self._products[product_id]
            return True
        return False

    def clear(self) -> None:
        """Wipe all records and reset the counter (used for test isolation)."""
        self._products.clear()
        self._current_id = 0


# Global singleton store instance for the application
product_store = ProductStore()
