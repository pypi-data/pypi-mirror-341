def merge_sort(arr: list[int]) -> list[int]:
    """
    Сортирует список целых чисел методом слияния и возвращает новый отсортированный список.

    Идея алгоритма:
    1. Рекурсивно делим список на две части, пока не останется по одному (или ноль) элементов.
    2. На этапе «слияния» объединяем две отсортированные части в один отсортированный список.
    Сложность в худшем и среднем случае: O(n log n), где n — размер списка.
    """
    if len(arr) <= 1:
        return arr  # База рекурсии: один элемент (или пустой список) уже «отсортирован»

    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    return merge(left_half, right_half)


def merge(left: list[int], right: list[int]) -> list[int]:
    """
    Сливает два отсортированных списка (left, right) в один отсортированный список.
    """
    i, j = 0, 0
    merged = []

    # Пока в обоих списках есть элементы, сравниваем и добавляем меньший
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # Если остались неиспользованные элементы в left или right, добавляем их
    merged.extend(left[i:])
    merged.extend(right[j:])

    return merged