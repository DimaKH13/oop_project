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
    sample_product.price = 2000.0
    assert sample_product.price == 2000.0

    sample_product.price = -100
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert sample_product.price == 2000.0

    sample_product.price = 0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert sample_product.price == 2000.0


def test_product_str(sample_product: Product) -> None:
    expected = "Test Phone, 1000.0 руб. Остаток: 10 шт."
    assert str(sample_product) == expected


def test_category_str(sample_category: Category, sample_product: Product) -> None:
    sample_category.add_product(sample_product)
    # Должно считать общее количество (10 + 10 = 20)
    expected = "Test Category, количество продуктов: 20 шт."
    assert str(sample_category) == expected


def test_product_add() -> None:
    p1 = Product("A", "Desc", 100.0, 10)
    p2 = Product("B", "Desc", 200.0, 2)
    # 100 * 10 + 200 * 2 = 1000 + 400 = 1400
    assert p1 + p2 == 1400.0
