"""Тестирование каталога"""
import database as db


def test_db_available():
    """Проверяет, что БД доступна."""
    try:
        products = db.get_all_products()
        return isinstance(products, list)
    except Exception as e:
        print(f"❌ БД недоступна: {e}")
        return False


def test_products_count():
    """Проверяет, что товары загружены."""
    products = db.get_all_products()
    return len(products) > 0


def test_product_fields():
    """Проверяет, что у всех товаров достаточно полей."""
    products = db.get_all_products()
    for p in products:
        if len(p) < 7:  # для библиотеки 7 полей
            print(f"❌ Товар id={p[0]}: мало полей ({len(p)})")
            return False
    return True


def test_prices_are_numbers():
    """Проверяет, что все цены — числа."""
    products = db.get_all_products()
    for p in products:
        # Индекс цены = 4
        if not isinstance(p[4], (int, float)):
            print(f"❌ Товар id={p[0]}: цена не число")
            return False
    return True


def test_quantity_not_negative():
    """Проверяет, что количество не отрицательное."""
    products = db.get_all_products()
    for p in products:
        # Индекс количества = 5
        if p[5] < 0:
            print(f"❌ Товар id={p[0]}: отрицательное количество")
            return False
    return True


def test_names_not_empty():
    """
    Проверяет, что у всех товаров есть название.

    ✅ ЗАДАНИЕ (ВЫПОЛНЕНО) — Пара 18, задание 6.6.
    """
    products = db.get_all_products()
    for p in products:
        # Индекс названия = 3
        if not p[3]:
            print(f"❌ Товар id={p[0]}: пустое название")
            return False
    return True


def test_has_image():
    """
    Проверяет, что хотя бы у одного товара есть обложка.


    """
    products = db.get_all_products()
    has_image = any(p[6] for p in products)  # индекс 6 = обложка
    return has_image


def run_all_tests():
    """Прогон всех тестов каталога."""
    tests = [
        ("БД доступна", test_db_available),
        ("Товары загружены", test_products_count),
        ("У всех товаров нужные поля", test_product_fields),
        ("Все цены — числа", test_prices_are_numbers),
        ("Количество не отрицательное", test_quantity_not_negative),
        ("Названия не пустые", test_names_not_empty),
        ("Хотя бы у одного товара есть обложка", test_has_image),
    ]


    print("ТЕСТИРОВАНИЕ КАТАЛОГА")


    passed = 0
    for name, func in tests:
        result = func()
        status = "✅" if result else "❌"
        if result:
            passed += 1
        print(f"{status} {name}")


    print(f"Пройдено: {passed} / {len(tests)}")

    if passed == len(tests):
        print("РЕЗУЛЬТАТ: ✅ УСПЕХ")
    else:
        print("РЕЗУЛЬТАТ: ❌ ЕСТЬ ОШИБКИ")



if __name__ == "__main__":
    run_all_tests()