import pytest

from src.models import Category, Product


@pytest.fixture(autouse=True)
def reset_counters() -> None:
    """Сбрасывает счетчики перед каждым тестом, чтобы они не мешали друг другу."""
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
    assert len(sample_category.products) == 1
    assert isinstance(sample_category.products[0], Product)


def test_category_counters(sample_product: Product) -> None:
    # Изначально счетчики должны быть на нуле (благодаря фикстуре reset_counters)
    assert Category.category_count == 0
    assert Category.product_count == 0

    # Создаем первую категорию с 2 продуктами
    Category("Cat 1", "Desc", [sample_product, sample_product])
    assert Category.category_count == 1
    assert Category.product_count == 2

    # Создаем вторую категорию с 1 продуктом
    Category("Cat 2", "Desc", [sample_product])
    assert Category.category_count == 2
    assert Category.product_count == 3
