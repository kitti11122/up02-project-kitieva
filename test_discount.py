"""Тестирование алгоритма скидки (вариант 25%) на данных библиотеки."""
from datetime import datetime
from discount import calculate_price_with_discount


def run_tests():
    """Прогон тестов."""
    print("=" * 75)
    print("ТЕСТИРОВАНИЕ АЛГОРИТМА СКИДКИ (вариант: 25% при отсутствии заказов)")
    print("=" * 75)

    passed = 0
    total = 0

   
    print("\n--- Группа 1: базовые тесты (дата 15.10.2026) ---")
    date1 = datetime(2026, 10, 15)
    cases1 = [
        (1, 1500, 1500, "«Война и мир» — есть заказ в сентябре → без скидки"),
        (2, 1200, 1200, "«Мастер и Маргарита» — есть заказ в сентябре → без скидки"),
        (3, 1000, 1000, "«Преступление и наказание» — есть заказ в сентябре → без скидки"),
        (4, 800, 600, "«Евгений Онегин» — нет заказов → скидка 25%"),
        (5, 2000, 1500, "«Властелин колец» — нет заказов → скидка 25%"),
    ]
    for product_id, price, expected, comment in cases1:
        result = calculate_price_with_discount(product_id, price, date1)
        status = "✅" if result == expected else "❌"
        total += 1
        if result == expected:
            passed += 1
        print(f"{status} Товар {product_id}: {price} → {result} "
              f"(ожидалось {expected}) — {comment}")

    
    print("\n--- Группа 2: новые тесты (разные даты) ---")

    # 15.11.2026 → предыдущий месяц = октябрь 2026, заказов нет → у всех скидка
    date2 = datetime(2026, 11, 15)
    cases2 = [
        (1, 1500, 1125, "15.11.2026 (окт.2026) — нет заказов → скидка 25%"),
        (3, 1000, 750, "15.11.2026 (окт.2026) — нет заказов → скидка 25%"),
    ]

    
    date3 = datetime(2026, 12, 15)
    cases3 = [
        (2, 1200, 900, "15.12.2026 (ноя.2026) — нет заказов → скидка 25%"),
        (6, 1800, 1350, "15.12.2026 (ноя.2026) — нет заказов → скидка 25%"),
    ]

   
    date4 = datetime(2027, 1, 15)
    cases4 = [
        (5, 2000, 1500, "15.01.2027 (дек.2026) — нет заказов → скидка 25%"),
    ]

    for date, cases in [(date2, cases2), (date3, cases3), (date4, cases4)]:
        for product_id, price, expected, comment in cases:
            result = calculate_price_with_discount(product_id, price, date)
            status = "✅" if result == expected else "❌"
            total += 1
            if result == expected:
                passed += 1
            print(f"{status} Товар {product_id}: {price} → {result} "
                  f"(ожидалось {expected}) — {comment}")

    print("\n" + "=" * 75)
    print(f"Пройдено: {passed} / {total}")
    print("=" * 75)


if __name__ == "__main__":
    run_tests()