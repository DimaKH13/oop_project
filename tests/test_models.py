import pytest

from src.models import Category, Product


@pytest.fixture(autouse=True)
def reset_counters() -> None:
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def sample_product() -> Product:
    return Product("Test Phone", "Good phone", 1000.0, 10)


@pytest.fixture
def sample_category(sample_product: Product) -> Category:
    return Category("Test Category", "Category desc", [sample_product])


def test_product_init(sample_product: Product) -> None:
    assert sample_product.name == "Test Phone"
    assert sample_product.description == "Good phone"
    assert sample_product.price == 1000.0
    assert sample_product.quantity == 10


def test_category_init(sample_category: Category) -> None:
    assert sample_category.name == "Test Category"
    assert sample_category.description == "Category desc"
    assert Category.category_count == 1
    assert Category.product_count == 1


def test_category_add_product(
    sample_category: Category, sample_product: Product
) -> None:
    assert Category.product_count == 1
    sample_category.add_product(sample_product)
    assert Category.product_count == 2
    # Проверяем, что товар добавился в строку
    assert sample_category.products.count("Test Phone") == 2


def test_product_new_product() -> None:
    data = {"name": "New Phone", "description": "Desc", "price": 500.0, "quantity": 5}
    new_prod = Product.new_product(data)
    assert isinstance(new_prod, Product)
    assert new_prod.name == "New Phone"
    assert new_prod.price == 500.0


def test_product_price_setter(
    sample_product: Product, capsys: pytest.CaptureFixture
) -> None:
    # Успешное изменение
    sample_product.price = 2000.0
    assert sample_product.price == 2000.0

    # Неуспешное изменение (отрицательное)
    sample_product.price = -100
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert sample_product.price == 2000.0  # Цена не изменилась

    # Неуспешное изменение (ноль)
    sample_product.price = 0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert sample_product.price == 2000.0
