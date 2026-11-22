from src.models import Category, Product

if __name__ == "__main__":
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)

    category = Category("Смартфоны", "Описание смартфонов", [product1, product2])

    print(f"Средняя цена в категории: {category.avg_price()}")

    empty_category = Category("Пустая", "Нет товаров", [])
    print(f"Средняя цена в пустой категории: {empty_category.avg_price()}")

    try:
        bad_product = Product("Брак", "Без количества", 1000.0, 0)
    except ValueError as e:
        print(f"Ошибка: {e}")
