from abc import ABC, abstractmethod
from typing import Any, Dict, List


class LoggingMixin:
    """Миксин для логирования создания объекта."""

    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        print(repr(self))

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}('{self.name}', "
            f"'{self.description}', {self.price}, {self.quantity})"
        )


class BaseProduct(ABC):
    """Базовый абстрактный класс для всех продуктов."""

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ) -> None:
        self.name = name
        self.description = description
        self._price = price
        self.quantity = quantity

    @property
    @abstractmethod
    def price(self) -> float:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


class Product(LoggingMixin, BaseProduct):
    """Базовый класс для представления товара."""

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ) -> None:
        super().__init__(name, description, price, quantity)

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, new_price: float) -> None:
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self._price = new_price

    @classmethod
    def new_product(cls, product_data: Dict[str, Any]) -> "Product":
        return cls(
            name=str(product_data["name"]),
            description=str(product_data["description"]),
            price=float(product_data["price"]),
            quantity=int(product_data["quantity"]),
        )

    def __str__(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных типов")
        return (self.price * self.quantity) + (other.price * other.quantity)


class Smartphone(Product):
    """Класс-наследник для смартфонов."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Класс-наследник для газонной травы."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


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
        if not isinstance(product, Product):
            raise TypeError(
                "В категорию можно добавлять только объекты класса Product "
                "и его наследников"
            )
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        result = ""
        for p in self.__products:
            result += f"{p}\n"
        return result

    def __str__(self) -> str:
        total_quantity = sum(p.quantity for p in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."
