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
from order_manager import (
    add_order_to_db,
    update_product_quantity,
    get_product_quantity
)


class ViewForm:
    """Форма просмотра выбранной книги."""

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

        author = self.product[2] if self.product[2] else "[Без автора]"
        title = self.product[3] if self.product[3] else "[Без названия]"
        genre = self.product[1] if self.product[1] else "[Без жанра]"
        price = self.product[4] if self.product[4] is not None else 0

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

        # Поле ввода количества
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
        
        """Обработчик кнопки «Добавить в заказ»."""

        # 1. Проверка товара
        if not self.product:
            messagebox.showerror("Ошибка", "Товар не выбран")
            return

        # 2. Валидация количества
        ok, result = validate_positive_int(
            self.qty_var.get(), "Количество")
        if not ok:
            messagebox.showwarning("Ошибка ввода", result)
            return

        qty = result
        product_id = int(self.product[0])

        # 3. Проверка остатка
        current_qty = get_product_quantity(product_id)
        if current_qty < 1:
            messagebox.showwarning(
                "Товар закончился",
                f"Книги «{self.product[3]}» больше нет")
            return

        if qty > current_qty:
            messagebox.showwarning(
                "Ошибка",
                f"Доступно только {current_qty} шт.")
            return

        # 4-5. Сохранение заказа + уменьшение остатка
        try:
            client = "Иванов Иван Иванович"  # заглушка
            order_id = add_order_to_db(client, product_id, qty)

            if order_id:
                new_qty = current_qty - qty
                update_product_quantity(product_id, new_qty)

                messagebox.showinfo(
                    "Успех",
                    f"Заказ №{order_id} оформлен!\n"
                    f"Книга «{self.product[3]}» × {qty} шт.")

                # 6. Обновить каталог
                if self.on_add_to_order:
                    self.on_add_to_order()

                self.window.destroy()
            else:
                messagebox.showerror(
                    "Ошибка",
                    "Не удалось сохранить заказ")

        except Exception as e:
            messagebox.showerror(
                "Ошибка заказа",
                f"Не удалось добавить товар:\n{e}")