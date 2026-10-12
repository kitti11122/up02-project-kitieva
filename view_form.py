"""Форма просмотра книги"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_HEADER, FONT_SIZE_TITLE, font
)
from resources import load_image, get_product_image
from discount import calculate_price_with_discount
from error_handler import validate_positive_int


class ViewForm:
    """
    Форма просмотра выбранной книги.
    Открывается при клике на карточку в каталоге.
    """

    def __init__(self, parent, product, on_add_to_order=None):
        self.product = product
        self.on_add_to_order = on_add_to_order

        self.window = tk.Toplevel(parent)
        self.window.title(f"Просмотр — {product[3]}")
        self.window.geometry("700x650")
        self.window.configure(bg=COLOR_MAIN_BG)

        self.build_ui()

    def build_ui(self):
        """Строит интерфейс формы."""
        # Шапка
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="КАРТОЧКА КНИГИ",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)

        # Основная область
        main = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # Изображение
        img_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        img_frame.pack(side="left", padx=10)

        try:
            photo = get_product_image(self.product[6], size=(200, 200))
            if photo:
                img_label = tk.Label(img_frame, image=photo,
                                      bg=COLOR_MAIN_BG)
                img_label.image = photo
                img_label.pack()
            else:
                tk.Label(img_frame, text="[НЕТ ФОТО]",
                         bg=COLOR_MAIN_BG, font=font(),
                         width=20, height=10).pack()
        except Exception as e:
            print(f"Ошибка загрузки фото: {e}")
            tk.Label(img_frame, text="[НЕТ ФОТО]",
                     bg=COLOR_MAIN_BG, font=font(),
                     width=20, height=10).pack()

        # Поля
        info_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        info_frame.pack(side="left", fill="both", expand=True, padx=20)

        # Обработка крайних случаев
        author = self.product[2] if self.product[2] else "[Без автора]"
        title = self.product[3] if self.product[3] else "[Без названия]"
        genre = self.product[1] if self.product[1] else "[Без жанра]"
        price = self.product[4] if self.product[4] is not None else 0

        # Цена со скидкой
        try:
            final_price = calculate_price_with_discount(
                int(self.product[0]), float(price), datetime.now())
        except Exception:
            final_price = price

        if final_price < price:
            price_text = (f"{final_price:.0f} руб. "
                          f"(скидка 25%, было {price:.0f})")
        else:
            price_text = f"{price:.0f} руб."

        self._add_field(info_frame, "Автор", author)
        self._add_field(info_frame, "Название", title)
        self._add_field(info_frame, "Жанр", genre)
        self._add_field(info_frame, "Цена со скидкой", price_text)
        self._add_field(info_frame, "В наличии",
                        f"{self.product[5]} шт.")


        qty_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        qty_frame.pack(pady=10)

        tk.Label(qty_frame, text="Количество:",
                 font=font(FONT_SIZE_NORMAL),
                 bg=COLOR_MAIN_BG).pack(side="left", padx=5)

        self.qty_var = tk.StringVar(value="1")
        tk.Entry(qty_frame, textvariable=self.qty_var, width=10,
                 font=font(FONT_SIZE_NORMAL)).pack(side="left")

        # Кнопки
        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        btn_frame.pack(fill="x", pady=10)

        tk.Button(btn_frame, text="Добавить в заказ",
                  command=self.add_to_order,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5).pack(side="left", padx=20)

        tk.Button(btn_frame, text="Назад",
                  command=self.window.destroy,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5).pack(side="right", padx=20)

    def _add_field(self, parent, label, value):
        """Добавляет поле в форму."""
        row = tk.Frame(parent, bg=COLOR_MAIN_BG)
        row.pack(fill="x", pady=3)

        tk.Label(row, text=f"{label}:",
                 font=font(FONT_SIZE_NORMAL, bold=True),
                 width=15, anchor="w",
                 bg=COLOR_MAIN_BG).pack(side="left")

        tk.Label(row, text=str(value),
                 font=font(FONT_SIZE_NORMAL),
                 anchor="w",
                 bg=COLOR_MAIN_BG).pack(side="left")

    def add_to_order(self):

        """Обработчик кнопки «Добавить в заказ»"""

        # 1. Проверка callback
        if not self.on_add_to_order:
            messagebox.showinfo("Информация",
                                 "Функция в разработке")
            return

        # 2. Проверка товара
        if not self.product:
            messagebox.showerror("Ошибка", "Товар не выбран")
            return

        # 3. Валидация количества через validate_positive_int
        ok, result = validate_positive_int(
            self.qty_var.get(), "Количество")
        if not ok:
            messagebox.showwarning("Ошибка ввода", result)
            return

        qty = result
        available = int(self.product[5])

        # 4. Проверка, что хватает на складе
        if qty > available:
            messagebox.showwarning(
                "Ошибка",
                f"В наличии только {available} шт.")
            return

        # 5. Обработка исключений
        try:
            self.on_add_to_order(self.product)
            messagebox.showinfo(
                "Успех",
                f"Книга «{self.product[3]}» × {qty} шт. "
                f"добавлена в заказ")
        except Exception as e:
            messagebox.showerror(
                "Ошибка заказа",
                f"Не удалось добавить товар:\n{e}")