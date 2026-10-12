"""Каталог книг (библиотека)"""
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
    Создаёт карточку книги по макету.

    :param parent: родительский контейнер
    :param product: кортеж с данными книги
    :param refresh: callback для обновления каталога
    :return: созданный Frame
    """
    qty = int(product[5])
    bg_color = _get_card_color(qty)

    card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x", padx=10, pady=5)

    _add_image(card, product, bg_color)
    _add_text_info(card, product, bg_color, qty)

    def on_click(event, p=product):
        _open_view(parent, p, refresh)

    card.bind("<Button-1>", on_click)
    for child in card.winfo_children():
        child.bind("<Button-1>", on_click)
        for sub in child.winfo_children():
            sub.bind("<Button-1>", on_click)

    return card


def _get_card_color(qty):
    """Возвращает цвет фона карточки (подсветка ≤3)."""
    return COLOR_HIGHLIGHT if qty <= 3 else COLOR_MAIN_BG


def _add_image(card, product, bg_color):
    """Добавляет изображение книги (или заглушку)."""
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)

    photo = get_product_image(product[6], size=(100, 100))

    if photo:
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.image = photo  # сохраняем ссылку!
        img_label.pack()
    else:
        tk.Label(img_frame, text="[НЕТ ФОТО]", bg=bg_color,
                 width=10, height=5).pack()


def _add_text_info(card, product, bg_color, qty):
    """Добавляет текстовую информацию о книге."""
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True,
                    padx=10, pady=10)

    author = product[2] if product[2] else "[Без автора]"
    title = product[3] if product[3] else "[Без названия]"
    genre = product[1] if product[1] else "[Без жанра]"
    price = product[4] if product[4] is not None else 0

    try:
        final_price = calculate_price_with_discount(
            int(product[0]), float(price), datetime.now())
    except Exception:
        final_price = price

    _add_label(text_frame, f"{author} | {title}",
               bg_color, bold=True, size=FONT_SIZE_HEADER)
    _add_label(text_frame, f"Жанр: {genre}", bg_color)
    _add_label(text_frame,
               f"Количество: {_indicator(qty)} ({qty})", bg_color)

    if final_price < price:
        price_text = (f"{final_price:.0f} руб. "
                      f"(скидка 25%, было {price:.0f})")
    else:
        price_text = f"{price:.0f} руб."

    _add_label(text_frame, price_text,
               bg_color, bold=True, size=FONT_SIZE_HEADER, align="e")


def _add_label(parent, text, bg_color, bold=False,
               size=FONT_SIZE_NORMAL, align="w"):
    """Добавляет метку с текстом."""
    tk.Label(parent, text=text, font=font(size, bold=bold),
             bg=bg_color, anchor=align).pack(fill="x")


def _indicator(qty):
    """Индикатор «много/мало» (порог 5)."""
    try:
        qty = int(qty)
    except (TypeError, ValueError):
        return "мало"
    return "много" if qty > 5 else "мало"


def _open_view(parent, product, refresh=None):
    """
    Открывает форму просмотра книги.

    ✅ ЗАДАНИЕ ДЛЯ СТУДЕНТА (ВЫПОЛНЕНО) — Пара 19-20.
    """
    from view_form import ViewForm
    ViewForm(parent, product, on_add_to_order=refresh)