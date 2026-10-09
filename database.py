"""Работа с базой данных."""
import sqlite3
from config import DB_PATH


def get_all_products():
    """Возвращает список кортежей из таблицы Товар."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return rows