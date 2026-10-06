"""Просмотр реальных данных моей БД (библиотека)."""
import sqlite3
from config import DB_PATH

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

print("=" * 70)
print("ТОВАРЫ (книги)")
print("=" * 70)
cur.execute("SELECT id, жанр, автор, название, цена, количество FROM Товар ORDER BY id")
for row in cur.fetchall():
    print(f"id={row[0]} | жанр={row[1]} | автор={row[2]} | {row[3]} | "
          f"цена={row[4]} | ост={row[5]}")

print("\n" + "=" * 70)
print("ЗАКАЗЫ")
print("=" * 70)
cur.execute(
    "SELECT id, дата, клиент, товар_id, количество "
    "FROM Заказ ORDER BY дата"
)
for row in cur.fetchall():
    print(f"id={row[0]} | {row[1]} | {row[2]} | товар_id={row[3]} | кол-во={row[4]}")

print("\n" + "=" * 70)
print("ЗАКАЗЫ ПО МЕСЯЦАМ (сколько заказов на каждый товар)")
print("=" * 70)
cur.execute("""
    SELECT товар_id, substr(дата, 1, 7) AS месяц, COUNT(*)
    FROM Заказ
    GROUP BY товар_id, месяц
    ORDER BY товар_id, месяц
""")
for row in cur.fetchall():
    print(f"товар_id={row[0]} | месяц={row[1]} | заказов={row[2]}")

conn.close()