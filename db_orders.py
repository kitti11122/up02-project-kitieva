"""Загрузка заказов из БД в объекты класса Order."""
import sqlite3
from config import DB_PATH
from models import Order
from db_products import get_all_products


def get_all_orders():
    """Возвращает список объектов Order из БД."""
    # Загружаем все товары в словарь {id: Product} для быстрого поиска
    products = {p.id: p for p in get_all_products()}

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, дата, клиент, товар_id, количество FROM Заказ ORDER BY id")
    rows = cur.fetchall()
    conn.close()

    orders = []
    for row in rows:
        product_id = int(row[3])
        product = products.get(product_id)

        # Если товар не найден — пропускаем заказ (или можно создать «заглушку»)
        if product is None:
            print(f"⚠️ Заказ №{row[0]}: товар с id={product_id} не найден")
            continue

        order = Order(
            order_id=int(row[0]),      # id
            date=row[1],               # дата
            client=row[2],             # клиент
            product=product,           # объект Product
            quantity=int(row[4])       # количество
        )
        orders.append(order)
    return orders


def print_orders(orders):
    """Выводит информацию о заказах и итоговую сумму."""
    print(f"\n{'=' * 70}")
    print(f"ЗАКАЗЫ ({len(orders)} шт.)")
    print("=" * 70)

    total_sum = 0
    for o in orders:
        print(o.info())
        print(f"    Цена за единицу: {o.product.price:.2f} ₽")
        print(f"    Сумма заказа:    {o.total():.2f} ₽")
        if not o.product.is_available():
            print("    ⚠️ Товар отсутствует на складе!")
        print("-" * 70)
        total_sum += o.total()

    print(f"ИТОГО по всем заказам: {total_sum:.2f} ₽")
    print("=" * 70)


if __name__ == "__main__":
    print_orders(get_all_orders())