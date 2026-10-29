import random
import time


# Генерация 1 000 000 товаров

N = 1_000_000

products = [
    {
        "id": random.randint(1, 10_000_000),
        "name": f"Товар_{i}"
    }
    for i in range(N)
]

random.shuffle(products)

print("Создано товаров:", len(products))
print("Пример:")
print(products[:5])


# Алгоритмы сортировки

def bubble_sort(arr):
    arr = arr.copy()
    n = len(arr)

    for i in range(n):
        swapped = False

        for j in range(0, n - i - 1):
            if arr[j]["id"] > arr[j + 1]["id"]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        if not swapped:
            break

    return arr


def selection_sort(arr):
    arr = arr.copy()
    n = len(arr)

    for i in range(n):
        min_index = i

        for j in range(i + 1, n):
            if arr[j]["id"] < arr[min_index]["id"]:
                min_index = j

        arr[i], arr[min_index] = arr[min_index], arr[i]

    return arr


def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]["id"]

    left = [x for x in arr if x["id"] < pivot]
    middle = [x for x in arr if x["id"] == pivot]
    right = [x for x in arr if x["id"] > pivot]

    return quick_sort(left) + middle + quick_sort(right)


# Замер времени сортировок

TEST_SIZE = 5000
test_products = products[:TEST_SIZE]

print("\n" + "=" * 60)
print("ЗАМЕР ВРЕМЕНИ СОРТИРОВОК")
print("=" * 60)

start = time.perf_counter()
bubble_result = bubble_sort(test_products)
bubble_time = time.perf_counter() - start

print(f"Пузырьковая сортировка: {bubble_time:.6f} секунд")


start = time.perf_counter()
selection_result = selection_sort(test_products)
selection_time = time.perf_counter() - start

print(f"Сортировка выбором:     {selection_time:.6f} секунд")


start = time.perf_counter()
quick_result = quick_sort(test_products)
quick_time = time.perf_counter() - start

print(f"Быстрая сортировка:     {quick_time:.6f} секунд")


# Проверка правильности сортировки

print("\nПроверка сортировки:")

print(
    "Пузырьковая:",
    all(
        bubble_result[i]["id"] <= bubble_result[i + 1]["id"]
        for i in range(len(bubble_result) - 1)
    )
)

print(
    "Выбором:",
    all(
        selection_result[i]["id"] <= selection_result[i + 1]["id"]
        for i in range(len(selection_result) - 1)
    )
)

print(
    "Быстрая:",
    all(
        quick_result[i]["id"] <= quick_result[i + 1]["id"]
        for i in range(len(quick_result) - 1)
    )
)


# Counting Sort для HTTP-статусов

def counting_sort_http(statuses):
    count = [0] * 500

    for status in statuses:
        count[status - 100] += 1

    result = []

    for i in range(500):
        for _ in range(count[i]):
            result.append(i + 100)

    return result


http_statuses = [
    random.randint(100, 599)
    for _ in range(10_000)
]

print("\n" + "=" * 60)
print("COUNTING SORT — HTTP-СТАТУСЫ")
print("=" * 60)

print("Первые 20 кодов до сортировки:")
print(http_statuses[:20])

start = time.perf_counter()

sorted_statuses = counting_sort_http(http_statuses)

counting_time = time.perf_counter() - start

print("\nПервые 20 кодов после сортировки:")
print(sorted_statuses[:20])

print(f"\nВремя Counting Sort: {counting_time:.6f} секунд")


# Группировка HTTP-кодов

groups = {}

for status in sorted_statuses:
    if status not in groups:
        groups[status] = 0

    groups[status] += 1

print("\nГруппировка HTTP-ответов:")

for status, count in groups.items():
    print(f"{status}: {count} запросов")


# Radix Sort для IPv4-адресов

def ip_to_number(ip):
    parts = list(map(int, ip.split(".")))

    return (
        (parts[0] << 24)
        | (parts[1] << 16)
        | (parts[2] << 8)
        | parts[3]
    )


def number_to_ip(number):
    return ".".join([
        str((number >> 24) & 255),
        str((number >> 16) & 255),
        str((number >> 8) & 255),
        str(number & 255)
    ])


def radix_sort_ips(ips):
    numbers = [ip_to_number(ip) for ip in ips]

    for shift in range(0, 32, 8):
        count = [0] * 256

        for number in numbers:
            byte = (number >> shift) & 255
            count[byte] += 1

        for i in range(1, 256):
            count[i] += count[i - 1]

        output = [0] * len(numbers)

        for i in range(len(numbers) - 1, -1, -1):
            number = numbers[i]
            byte = (number >> shift) & 255

            count[byte] -= 1
            output[count[byte]] = number

        numbers = output

    return [number_to_ip(number) for number in numbers]


ips = [
    f"{random.randint(0, 255)}."
    f"{random.randint(0, 255)}."
    f"{random.randint(0, 255)}."
    f"{random.randint(0, 255)}"
    for _ in range(10_000)
]

print("\n" + "=" * 60)
print("RADIX SORT — IP-АДРЕСА")
print("=" * 60)

print("Первые 20 IP до сортировки:")
print(ips[:20])

start = time.perf_counter()

sorted_ips = radix_sort_ips(ips)

radix_time = time.perf_counter() - start

print("\nПервые 20 IP после сортировки:")
print(sorted_ips[:20])

print(f"\nВремя Radix Sort: {radix_time:.6f} секунд")


# Итоговая таблица

print("\n" + "=" * 60)
print("ИТОГОВАЯ ТАБЛИЦА")
print("=" * 60)

print(f"{'Алгоритм':<25} {'Количество':<15} {'Время, сек':<15}")
print("-" * 55)

print(f"{'Bubble Sort':<25} {TEST_SIZE:<15} {bubble_time:<15.6f}")
print(f"{'Selection Sort':<25} {TEST_SIZE:<15} {selection_time:<15.6f}")
print(f"{'Quick Sort':<25} {TEST_SIZE:<15} {quick_time:<15.6f}")
print(f"{'Counting Sort':<25} {10000:<15} {counting_time:<15.6f}")
print(f"{'Radix Sort':<25} {10000:<15} {radix_time:<15.6f}")
