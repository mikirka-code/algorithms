import time
import random
import math


# 1. Генерация товаров


N = 1_000_000

products = [
    {
        "id": i,
        "name": f"Товар_{i}"
    }
    for i in range(1, N + 1)
]

print(f"Создано товаров: {len(products)}")



# 2. ЛИНЕЙНЫЙ ПОИСК


def linear_search(products, target):
    for product in products:
        if product["id"] == target:
            return product
    return None



# 3. ЭКСПОНЕНЦИАЛЬНЫЙ ПОИСК


def exponential_search(products, target):
    n = len(products)

    if n == 0:
        return None

    if products[0]["id"] == target:
        return products[0]

    index = 1

    while index < n and products[index]["id"] <= target:
        index *= 2

    left = index // 2
    right = min(index, n - 1)

    while left <= right:
        middle = (left + right) // 2

        if products[middle]["id"] == target:
            return products[middle]

        elif products[middle]["id"] < target:
            left = middle + 1

        else:
            right = middle - 1

    return None



# 4. БИНАРНЫЙ ПОИСК


def binary_search(products, target):
    left = 0
    right = len(products) - 1

    while left <= right:
        middle = (left + right) // 2

        if products[middle]["id"] == target:
            return products[middle]

        elif products[middle]["id"] < target:
            left = middle + 1

        else:
            right = middle - 1

    return None



# 5. ПРЫЖКОВЫЙ ПОИСК

def jump_search(products, target):
    n = len(products)

    step = int(math.sqrt(n))

    left = 0
    right = step

    while left < n and products[min(right, n) - 1]["id"] < target:
        left = right
        right += step

        if left >= n:
            return None

    for i in range(left, min(right, n)):
        if products[i]["id"] == target:
            return products[i]

    return None



# 6. Артикулы для поиска

random_id = random.randint(2, N - 1)

searches = [
    ("Начало списка", 1),
    ("Середина списка", N // 2),
    ("Конец списка", N),
    ("Случайный элемент", random_id),
    ("Отсутствующий", N + 1)
]



# 7. Алгоритмы


algorithms = {
    "Линейный": linear_search,
    "Экспоненциальный": exponential_search,
    "Бинарный": binary_search,
    "Прыжковый": jump_search
}



# 8. Измерение времени


results = []

for algorithm_name, algorithm in algorithms.items():

    for search_name, target in searches:

        start = time.perf_counter()

        result = algorithm(products, target)

        end = time.perf_counter()

        elapsed = end - start

        results.append([
            algorithm_name,
            search_name,
            target,
            elapsed,
            "Да" if result else "Нет"
        ])



# 9. Итоговая таблица

print("\n" + "=" * 90)
print("РЕЗУЛЬТАТЫ")
print("=" * 90)

print(
    f"{'Алгоритм':<20}"
    f"{'Тип поиска':<25}"
    f"{'Артикул':<12}"
    f"{'Время (сек)':<18}"
    f"{'Найден':<10}"
)

print("-" * 90)

for result in results:
    print(
        f"{result[0]:<20}"
        f"{result[1]:<25}"
        f"{result[2]:<12}"
        f"{result[3]:<18.10f}"
        f"{result[4]:<10}"
    )


# 10. Среднее время

print("\n" + "=" * 50)
print("СРЕДНЕЕ ВРЕМЯ ПО АЛГОРИТМАМ")
print("=" * 50)

for algorithm_name in algorithms:

    times = [
        result[3]
        for result in results
        if result[0] == algorithm_name
    ]

    average = sum(times) / len(times)

    print(f"{algorithm_name:<20} {average:.10f} сек")
