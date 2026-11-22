import pytest

from src.models import BaseProduct, Category, LawnGrass, Product, Smartphone


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


def test_zero_quantity_error() -> None:
    with pytest.raises(ValueError):
        Product("Bad Phone", "Desc", 100.0, 0)


def test_category_avg_price(sample_category: Category, sample_product: Product) -> None:
    p2 = Product("Phone 2", "Desc", 2000.0, 5)
    sample_category.add_product(p2)
    assert sample_category.avg_price() == 1500.0


def test_category_avg_price_empty() -> None:
    empty_category = Category("Empty", "Desc", [])
    assert empty_category.avg_price() == 0


def test_base_product_is_abstract() -> None:
    with pytest.raises(TypeError):
        BaseProduct("Name", "Desc", 100.0, 1)  # type: ignore


def test_product_init(sample_product: Product) -> None:
    assert sample_product.name == "Test Phone"
    assert sample_product.price == 1000.0
    assert sample_product.quantity == 10


def test_category_init(sample_category: Category) -> None:
    assert sample_category.name == "Test Category"
    assert Category.category_count == 1
    assert Category.product_count == 1


def test_product_price_setter(
    sample_product: Product, capsys: pytest.CaptureFixture
) -> None:
    sample_product.price = 2000.0
    assert sample_product.price == 2000.0
    sample_product.price = -100
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out


def test_product_str(sample_product: Product) -> None:
    expected = "Test Phone, 1000.0 руб. Остаток: 10 шт."
    assert str(sample_product) == expected


def test_product_add(sample_product: Product) -> None:
    p2 = Product("B", "Desc", 200.0, 2)
    assert sample_product + p2 == 10400.0


def test_add_different_types_error() -> None:
    phone = Smartphone("iPhone", "Desc", 1000.0, 1, 99.0, "15", 256, "Black")
    grass = LawnGrass("Grass", "Desc", 500.0, 10, "Russia", "5 days", "Green")
    with pytest.raises(TypeError):
        phone + grass


def test_add_product_type_error(sample_category: Category) -> None:
    with pytest.raises(TypeError):
        sample_category.add_product("Not a product")  # type: ignore
