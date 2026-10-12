"""Тестирование индикатора «много/мало» (Пара 13 + Пара 18)."""
from catalog import _indicator


def test_indicator():
    """Прогон тестов для индикатора."""
    test_cases = [
        # Базовые 5 тестов
        (10, "много", "10 > 5"),
        (6, "много", "6 > 5"),
        (5, "мало", "5 ≤ 5 (граница!)"),
        (4, "мало", "4 ≤ 5"),
        (0, "мало", "0 ≤ 5"),

        # ✅ Дописанные 3 теста (Пара 18)
        (100, "много", "большое число"),
        (1, "мало", "минимальное > 0"),
        (-1, "мало", "отрицательное (крайний случай)"),
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
    print("=" * 60)


if __name__ == "__main__":
    test_indicator()