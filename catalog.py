"""Каталог книг (библиотека).

============================================================
ЗАДАНИЕ ДЛЯ СТУДЕНТА (ВЫПОЛНЕНО) — Задания 4.4 и 7.4:
1. ✅ Импорт стилей из styles.py
2. ✅ Импорт get_product_image из resources.py
3. ✅ Карточка книги с подсветкой и скидкой
============================================================
"""
import tkinter as tk
from datetime import datetime

from styles import (
    COLOR_MAIN_BG, COLOR_HIGHLIGHT,
    FONT_SIZE_NORMAL, FONT_SIZE_HEADER,
    font
)
from resources import get_product_image
from discount import calculate_price_with_discount


def create_product_card(parent, product, refresh=None):
    """
    Создаёт карточку книги.

    Индексы таблицы Товар (библиотека):
    [0] id, [1] жанр, [2] автор, [3] название,
    [4] цена, [5] количество, [6] обложка

    :param parent: родительский контейнер
    :param product: кортеж с данными книги
    :param refresh: callback для обновления каталога
    :return: созданный Frame
    """
    product_id = int(product[0])
    genre = product[1]
    author = product[2]
    title = product[3]
    price = float(product[4])
    qty = int(product[5])
    cover = product[6]

    # Подсветка, если количество ≤3
    bg_color = COLOR_HIGHLIGHT if qty <= 3 else COLOR_MAIN_BG

    # Цена со скидкой 25%
    try:
        final_price = calculate_price_with_discount(
            product_id, price, datetime.now())
    except Exception:
        final_price = price

    # Карточка — рамка со всех сторон
    card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x", padx=10, pady=5)

    # === Изображение (слева) ===
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)

    # Получаем изображение через функцию из resources
    photo = get_product_image(cover, size=(100, 100))

    if photo:
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.image = photo  # сохраняем ссылку!
        img_label.pack()
    else:
        tk.Label(img_frame, text="[НЕТ ФОТО]", bg=bg_color,
                 width=10, height=5).pack()

    # === Текстовая часть (справа) ===
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True,
                    padx=10, pady=10)

    # Автор | Название (жирно)
    tk.Label(text_frame, text=f"{author} | {title}",
             font=font(FONT_SIZE_HEADER, bold=True),
             bg=bg_color, anchor="w").pack(fill="x")

    # Жанр
    tk.Label(text_frame, text=f"Жанр: {genre}",
             font=font(), bg=bg_color,
             anchor="w").pack(fill="x")

    # Количество
    indicator = "много" if qty > 5 else "мало"
    tk.Label(text_frame, text=f"Количество: {indicator} ({qty})",
             font=font(), bg=bg_color,
             anchor="w").pack(fill="x")

    # Цена
    if final_price < price:
        price_text = (f"{final_price:.0f} руб. "
                      f"(скидка 25%, было {price:.0f})")
    else:
        price_text = f"{price:.0f} руб."

    tk.Label(text_frame, text=price_text,
             font=font(FONT_SIZE_HEADER, bold=True),
             bg=bg_color, anchor="e").pack(fill="x")

    # Разделитель между карточками
    tk.Frame(parent, height=2, bd=1,
             relief="sunken").pack(fill="x", padx=5)

    return card