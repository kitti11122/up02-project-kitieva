"""Загрузка товаров из БД с расширенным выводом."""
import sqlite3
from config import DB_PATH


def get_all_products():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар ORDER BY id")
    products = cur.fetchall()
    conn.close()
    return products


def get_products_by_category(category):
    """Товары по жанру."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # Ищем по колонке 'жанр'
    cur.execute("SELECT * FROM Товар WHERE жанр = ?", (category,))
    products = cur.fetchall()
    conn.close()
    return products


def get_products_low_stock():
    """Товары с количеством ≤ 3."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE количество <= 3")
    products = cur.fetchall()
    conn.close()
    return products


def get_categories():
    """Список всех жанров."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # Берем уникальные значения из колонки 'жанр'
    cur.execute("SELECT DISTINCT жанр FROM Товар ORDER BY жанр")
    categories = [row[0] for row in cur.fetchall()]
    conn.close()
    return categories


def print_catalog(products):
    """Каталог с индикатором."""
    print(f"\n{'=' * 60}")
    print(f"КАТАЛОГ ({len(products)} товаров)")
    print("=" * 60)

    for p in products:
        # Индексы под вашу таблицу:
        # p[0] = id
        # p[1] = жанр
        # p[2] = автор
        # p[3] = название
        # p[4] = цена
        # p[5] = количество
        # p[6] = обложка
        
        genre = p[1]
        author = p[2]
        name = p[3]
        price = p[4]
        qty = p[5]

        # Преобразуем в числа на случай, если БД вернула строки
        try:
            price = float(price)
            qty = int(qty)
        except (ValueError, TypeError):
            print(f"⚠️ Ошибка данных: {name} — цена: {price}, кол-во: {qty}")
            continue

        indicator = "много" if qty > 5 else "мало"
        highlight = "⚠️" if qty <= 3 else "  "

        # Выводим: Название (Жанр, Автор)
        print(f"{highlight} {name} ({genre}, {author})")
        print(f"   Цена: {price} руб. | Кол-во: {qty} ({indicator})")

    print("=" * 60)


if __name__ == "__main__":
    print("1. Все товары")
    print_catalog(get_all_products())

    print("\n2. Жанры:")
    for cat in get_categories():
        print(f"   - {cat}")

    print("\n3. Товары с низким остатком (≤3):")
    print_catalog(get_products_low_stock())