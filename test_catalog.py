"""Проверка вывода полей"""
import database as db


def test_fields():
    """Проверяет, что все поля на месте."""
    products = db.get_all_products()
    print(f"Всего товаров: {len(products)}")

    required_count = 7  # для библиотеки 7 полей
    errors = 0

    for p in products:
        if len(p) < required_count:
            print(f"❌ Товар id={p[0]}: мало полей ({len(p)})")
            errors += 1

    if errors == 0:
        print("✅ Все товары содержат нужные поля")
    else:
        print(f"❌ Найдено ошибок: {errors}")


def test_prices():
    """
    Проверяет, что у всех товаров есть цена.

    ✅ ЗАДАНИЕ ИЗ ДЗ (ВЫПОЛНЕНО).
    """
    products = db.get_all_products()

    for p in products:
        # Индекс цены — 4
        if p[4] is None:
            print(f"❌ Товар id={p[0]}: нет цены")
            return

    print("✅ У всех товаров есть цена")


def test_quantities():
    """
    Проверяет, что количество ≥ 0.

    ✅ ЗАДАНИЕ ИЗ ДЗ (ВЫПОЛНЕНО).
    """
    products = db.get_all_products()

    for p in products:
        # Индекс количества — 5
        if p[5] is None or p[5] < 0:
            print(f"❌ Товар id={p[0]}: некорректное количество")
            return

    print("✅ У всех товаров количество ≥ 0")


def test_has_images():
    """
    Проверяет, что хотя бы у одной книги есть обложка.

    ✅ ЗАДАНИЕ ИЗ ДЗ (ВЫПОЛНЕНО).
    """
    products = db.get_all_products()

    has_image = any(p[6] for p in products)  # индекс 6 — обложка

    if has_image:
        print("✅ Хотя бы у одной книги есть обложка")
    else:
        print("❌ Ни у одной книги нет обложки")


if __name__ == "__main__":
    print("=" * 50)
    print("ТЕСТИРОВАНИЕ КАТАЛОГА")
    print("=" * 50)

    test_fields()
    test_prices()
    test_quantities()
    test_has_images()

    print("=" * 50)
    print("Тестирование завершено")
    print("=" * 50)