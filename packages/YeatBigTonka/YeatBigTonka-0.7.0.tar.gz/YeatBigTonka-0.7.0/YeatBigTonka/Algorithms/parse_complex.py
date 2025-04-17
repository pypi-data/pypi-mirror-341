import re


def parse_complex(s: str) -> tuple[float, float]:
    """
    Разбирает строку комплексного числа в формате 'a + i*b' или 'a - i*b'
    и возвращает кортеж (real, imag) вещественной и мнимой частей в виде float.
    Пример корректного ввода: '3 + i*4', '-2 - i*10', '0 + i*1'.
    """
    # Убираем пробелы
    s = s.replace(" ", "")
    # Регулярное выражение для форматов вида:
    # '3+i*4', '-2-i*10', '0+i*1' и т.п.
    pattern = r'^([+-]?\d+)([+-])i\*([+-]?\d+)$'
    match = re.match(pattern, s)

    if not match:
        raise ValueError(
            "Неверный формат комплексного числа. "
            "Ожидается что-то вроде '3 + i*4' или '-2 - i*10'."
        )

    real_str, sign, imag_str = match.groups()

    real_part = float(real_str)
    imag_part = float(imag_str)

    # Если стоит минус между действительной и мнимой частями — мнимая часть отрицательная
    if sign == '-':
        imag_part = -imag_part

    return real_part, imag_part


def add_complex(c1: tuple[float, float], c2: tuple[float, float]) -> tuple[float, float]:
    """Сумма комплексных чисел c1 и c2."""
    return (c1[0] + c2[0], c1[1] + c2[1])


def sub_complex(c1: tuple[float, float], c2: tuple[float, float]) -> tuple[float, float]:
    """Разность комплексных чисел c1 и c2 (c1 - c2)."""
    return (c1[0] - c2[0], c1[1] - c2[1])


def mul_complex(c1: tuple[float, float], c2: tuple[float, float]) -> tuple[float, float]:
    """
    Произведение комплексных чисел c1 и c2.
    Пусть c1 = (a, b), c2 = (c, d).
    Тогда (a + bi)*(c + di) = (ac - bd) + i(ad + bc).
    """
    a, b = c1
    c, d = c2
    real_part = a * c - b * d
    imag_part = a * d + b * c
    return (real_part, imag_part)
