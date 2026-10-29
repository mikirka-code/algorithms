# Лабораторная работа 5. Графы. Алгоритм Дейкстры и алгоритм Флойда-Уоршелла

import heapq


# Время перегона на каждой линии (в минутах)
GREEN = 4       # зелёная
PURPLE = 5      # фиолетовая
BLUE = 6        # синяя
RED = 3         # красная
YELLOW = 2      # жёлтая (оранжевая на картинке)
TRANSFER = 1    # переход между станциями

# Рёбра графа: (станция, станция, время в минутах)
edges = [
    # Красная линия
    ("Площадь Восстания", "Владимирская", RED),
    ("Владимирская", "Пушкинская", RED),
    ("Пушкинская", "Технологический институт", RED),

    # Синяя линия
    ("Невский проспект", "Сенная площадь", BLUE),
    ("Сенная площадь", "Технологический институт", BLUE),

    # Зелёная линия
    ("Гостиный двор", "Маяковская", GREEN),
    ("Маяковская", "Площадь Александра Невского", GREEN),

    # Жёлтая линия
    ("Спасская", "Достоевская", YELLOW),
    ("Достоевская", "Лиговский проспект", YELLOW),
    ("Лиговский проспект", "Площадь Александра Невского", YELLOW),
    ("Площадь Александра Невского", "Новочеркасская", YELLOW),
    ("Новочеркасская", "Ладожская", YELLOW),
    ("Ладожская", "Проспект Большевиков", YELLOW),

    # Фиолетовая линия
    ("Адмиралтейская", "Садовая", PURPLE),
    ("Садовая", "Звенигородская", PURPLE),
    ("Звенигородская", "Обводный канал", PURPLE),

    # Переходы между станциями
    ("Невский проспект", "Гостиный двор", TRANSFER),
    ("Площадь Восстания", "Маяковская", TRANSFER),
    ("Владимирская", "Достоевская", TRANSFER),
    ("Пушкинская", "Звенигородская", TRANSFER),
    ("Сенная площадь", "Спасская", TRANSFER),
    ("Сенная площадь", "Садовая", TRANSFER),
    ("Спасская", "Садовая", TRANSFER),
]


# Строим граф: станция -> {соседняя станция: время}
metro = {}
for a, b, time in edges:
    metro.setdefault(a, {})[b] = time
    metro.setdefault(b, {})[a] = time   # метро ездит в обе стороны


# Алгоритм Дейкстры: кратчайший путь от одной станции до другой
def dijkstra(graph, start, end):
    # Расстояние до всех станций сначала "бесконечность", до старта — 0
    dist = {station: float("inf") for station in graph}
    dist[start] = 0
    parents = {start: None}   # откуда пришли в каждую станцию
    visited = set()

    # Очередь с приоритетом: (расстояние, станция), сверху всегда самая близкая
    heap = [(0, start)]

    while heap:
        # Берём ещё не обработанную станцию с наименьшим расстоянием
        d, station = heapq.heappop(heap)
        if station in visited:
            continue
        visited.add(station)

        # До конечной станции дошли — расстояние до неё уже точно минимальное
        if station == end:
            break

        # Пробуем улучшить расстояние до соседей через текущую станцию
        for neighbor, time in graph[station].items():
            new_dist = d + time
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                parents[neighbor] = station
                heapq.heappush(heap, (new_dist, neighbor))

    # Если до конечной станции не добрались — пути нет
    if dist[end] == float("inf"):
        return None, None

    # Восстанавливаем путь, идя от конца к началу по parents
    path = []
    station = end
    while station is not None:
        path.append(station)
        station = parents[station]
    path.reverse()

    return path, dist[end]


# Алгоритм Флойда-Уоршелла: кратчайшие пути между ВСЕМИ парами станций
def floyd_warshall(graph):
    stations = list(graph)

    # dist[a][b] — лучшее известное время от a до b
    # next_station[a][b] — куда ехать первым шагом из a, чтобы попасть в b
    dist = {a: {b: float("inf") for b in stations} for a in stations}
    next_station = {a: {b: None for b in stations} for a in stations}

    # Начальные значения: 0 до самой себя и время перегона до соседей
    for a in stations:
        dist[a][a] = 0
        next_station[a][a] = a
        for b, time in graph[a].items():
            dist[a][b] = time
            next_station[a][b] = b

    # Для каждой промежуточной станции k проверяем:
    # не быстрее ли ехать из a в b через k
    for k in stations:
        for a in stations:
            for b in stations:
                if dist[a][k] + dist[k][b] < dist[a][b]:
                    dist[a][b] = dist[a][k] + dist[k][b]
                    next_station[a][b] = next_station[a][k]

    return dist, next_station


# Восстановление пути из таблиц Флойда-Уоршелла
def floyd_path(dist, next_station, start, end):
    if next_station[start][end] is None:
        return None, None

    # Идём шаг за шагом по таблице "следующая станция"
    path = [start]
    station = start
    while station != end:
        station = next_station[station][end]
        path.append(station)

    return path, dist[start][end]


# Правильное окончание слова "минута"
def minutes_word(n):
    if n % 10 == 1 and n % 100 != 11:
        return "минута"
    if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14):
        return "минуты"
    return "минут"


# Вывод результата в виде "Станция->Станция, 6 минут"
def print_result(title, path, time):
    if path is None:
        print(title, "пути нет")
    else:
        print(title, "->".join(path) + ",", time, minutes_word(time))


# Поиск станции по введённому названию без учёта регистра
def find_station(graph, name):
    for station in graph:
        if station.lower() == name.strip().lower():
            return station
    return None


# Флойда-Уоршелла считаем один раз сразу для всех пар станций
fw_dist, fw_next = floyd_warshall(metro)

# Пример из задания
print("Вход: Спасская, Пушкинская")
path, time = dijkstra(metro, "Спасская", "Пушкинская")
print_result("Дейкстра:         ", path, time)
path, time = floyd_path(fw_dist, fw_next, "Спасская", "Пушкинская")
print_result("Флойд-Уоршелл:    ", path, time)


# Ввод своих станций с клавиатуры
print("\nСтанции:", ", ".join(metro))
while True:
    line = input("\nВведите две станции через запятую (пустая строка — выход): ")
    line = line.replace("﻿", "")  # убираем невидимый символ BOM, если ввод пришёл из файла
    if line.strip() == "":
        break

    parts = line.split(",")
    if len(parts) != 2:
        print("Нужно ввести ровно две станции через запятую")
        continue

    start = find_station(metro, parts[0])
    end = find_station(metro, parts[1])
    if start is None or end is None:
        print("Такой станции нет в графе")
        continue

    path, time = dijkstra(metro, start, end)
    print_result("Дейкстра:         ", path, time)
    path, time = floyd_path(fw_dist, fw_next, start, end)
    print_result("Флойд-Уоршелл:    ", path, time)
