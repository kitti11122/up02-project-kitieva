"""Модели данных для проекта УП.02."""
from datetime import datetime
from discount import calculate_price_with_discount


class Product:
    """Класс Товар."""

    def __init__(self, product_id, name, category, price, quantity):
        """
        Инициализация товара.

        :param product_id: идентификатор
        :param name: название
        :param category: категория
        :param price: цена
        :param quantity: количество
        """
        self.id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity

    def total(self):
        """Общая стоимость (цена × количество)."""
        return self.price * self.quantity

    def price_with_discount(self, discount_percent):
        """Цена со скидкой (ручной процент)."""
        return self.price * (1 - discount_percent / 100)

    def price_with_discount_auto(self, date=None):
        """Цена со скидкой по алгоритму ДЭ (25%, если не было заказов в прошлом месяце)."""
        if date is None:
            date = datetime.now()
        return calculate_price_with_discount(self.id, self.price, date)

    def discounted_price(self):
        """Цена со скидкой 25% (упрощённо)."""
        return self.price * 0.75

    def indicator(self):
        """Индикатор «много/мало» (порог 5)."""
        return "много" if self.quantity > 5 else "мало"

    def is_available(self):
        """True, если товар есть в наличии (количество > 0)."""
        return self.quantity > 0

    def info(self):
        """Строка с информацией о товаре."""
        return (
            f"{self.name} ({self.category}): "
            f"{self.price} руб. × {self.quantity} = {self.total()} руб. "
            f"({self.indicator()})"
        )


class Order:
    """Класс Заказ."""

    def __init__(self, order_id, date, client, product, quantity):
        """
        Инициализация заказа.

        :param order_id: номер заказа
        :param date: дата заказа
        :param client: имя клиента
        :param product: объект Product
        :param quantity: количество единиц товара в заказе
        """
        self.id = order_id
        self.date = date
        self.client = client
        self.product = product      # объект Product
        self.quantity = quantity

    def total(self):
        """Стоимость заказа."""
        return self.product.price * self.quantity

    def info(self):
        """Строка с информацией о заказе."""
        return (
            f"Заказ №{self.id} от {self.date}: "
            f"{self.client} — {self.product.name} × {self.quantity}"
        )

    def order_info(self):
        """Краткая информация о заказе (без товара)."""
        return f"Заказ №{self.id} от {self.date}: {self.client}"