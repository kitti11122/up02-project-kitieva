"""Загрузка товаров из БД в объекты класса Product."""
import sqlite3
from config import DB_PATH
from models import Product


def get_all_products():
    """Возвращает список объектов Product из БД."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар ORDER BY id")
    rows = cur.fetchall()
    conn.close()

    products = []
    for row in rows:
        # Реальная структура таблицы: id, жанр, автор, название, цена, количество, обложка
        product = Product(
            product_id=int(row[0]),   # id
            name=row[3],              # название
            category=row[1],          # жанр (используем как категорию)
            price=float(row[4]),      # цена
            quantity=int(row[5])      # количество
        )
        products.append(product)
    return products


def get_products_by_category(category):
    """Возвращает список объектов Product по категории (жанру)."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE жанр = ?", (category,))
    rows = cur.fetchall()
    conn.close()

    products = []
    for row in rows:
        product = Product(
            product_id=int(row[0]),
            name=row[3],
            category=row[1],
            price=float(row[4]),
            quantity=int(row[5])
        )
        products.append(product)
    return products


def get_products_low_stock():
    """Возвращает товары с количеством ≤ 3."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE количество <= 3")
    rows = cur.fetchall()
    conn.close()

    products = []
    for row in rows:
        product = Product(
            product_id=int(row[0]),
            name=row[3],
            category=row[1],
            price=float(row[4]),
            quantity=int(row[5])
        )
        products.append(product)
    return products


def print_products(products):
    """Выводит информацию о товарах."""
    print(f"\nВсего товаров: {len(products)}\n")
    for p in products:
        print(p.info())
        print("-" * 60)


def print_catalog_with_highlight(products):
    """Выводит каталог с подсветкой для товаров ≤3."""
    print(f"\n{'=' * 70}")
    print(f"КАТАЛОГ ({len(products)} товаров)")
    print("=" * 70)

    for p in products:
        highlight = "⚠️" if p.quantity <= 3 else "  "
        print(f"{highlight} {p.info()}")

    print("=" * 70)


if __name__ == "__main__":
    print("1. Все товары:")
    print_catalog_with_highlight(get_all_products())

    print("\n2. Товары жанра «Роман»:")
    print_catalog_with_highlight(get_products_by_category("Роман"))

    print("\n3. Товары с низким остатком (≤3):")
    print_catalog_with_highlight(get_products_low_stock())