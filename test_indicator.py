"""Тестирование индикатора «много/мало»"""
from catalog import _indicator


def test_indicator():
    """Прогон тестов для индикатора."""
    test_cases = [
        # (qty, expected, comment)

     
        (10, "много", "10 > 5"),
        (6, "много", "6 > 5 (граница)"),
        (5, "мало", "5 ≤ 5 (граница)"),
        (4, "мало", "4 ≤ 5"),
        (1, "мало", "1 ≤ 5"),
        (0, "мало", "0 ≤ 5"),
        (100, "много", "большое число"),

       
        (1000, "много", "qty=1000 — очень большое число"),
        (50, "много", "qty=50 — среднее значение"),
        (5, "мало", "qty=5 — повторно (граница)"),
        (6, "много", "qty=6 — повторно (граница)"),
        (-1, "мало", "qty=-1 — отрицательное → мало"),
    ]

    print("=" * 60)
    print("ТЕСТИРОВАНИЕ ИНДИКАТОРА")
    print("=" * 60)

    passed = 0
    for qty, expected, comment in test_cases:
        result = _indicator(qty)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        print(f"{status} qty={qty}: {result} "
              f"(ожидалось {expected}) — {comment}")

    print("=" * 60)
    print(f"Пройдено: {passed} / {len(test_cases)}")

    if passed == len(test_cases):
        print("РЕЗУЛЬТАТ: ✅ УСПЕХ")
    else:
        print("РЕЗУЛЬТАТ: ❌ ЕСТЬ ОШИБКИ")
    print("=" * 60)


if __name__ == "__main__":
    test_indicator()