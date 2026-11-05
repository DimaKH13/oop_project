from typing import Any, Dict, List


class Product:
    """Класс для представления товара."""

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ) -> None:
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @classmethod
    def new_product(cls, product_data: Dict[str, Any]) -> "Product":
        """Класс-метод для создания товара из словаря."""
        return cls(
            name=str(product_data["name"]),
            description=str(product_data["description"]),
            price=float(product_data["price"]),
            quantity=int(product_data["quantity"]),
        )

    @property
    def price(self) -> float:
        """Геттер для цены."""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Сеттер для цены с проверкой на положительное значение."""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = new_price

    def __str__(self) -> str:
        """Строковое представление товара."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        """Магический метод сложения: возвращает общую стоимость товаров на складе."""
        return (self.price * self.quantity) + (other.price * other.quantity)


class Category:
    """Класс для представления категории товаров."""

    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: List[Product]) -> None:
        self.name = name
        self.description = description
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product: Product) -> None:
        """Добавляет продукт в приватный список и увеличивает счетчик."""
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Геттер, возвращающий строку со всеми продуктами."""
        result = ""
        for p in self.__products:
            result += f"{p}\n"  # Используем магический метод __str__ продукта
        return result

    def __str__(self) -> str:
        """Строковое представление категории."""
        # Считаем общее количество товаров на складе
        total_quantity = sum(p.quantity for p in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."
