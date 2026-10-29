# A. Проверка, является ли один массив подмножеством другого

def is_subset(big_array, small_array):
    hash_table = {}

    # Заполняем хэш-таблицу Эл. Бол. М. И проверяем
    for item in big_array:
        hash_table[item] = True

    for item in small_array:
        if item not in hash_table:
            return False

    return True


print("A:")
print(is_subset(["a", "b", "c", "d", "e", "f"], ["b", "d", "f"]))
print(is_subset(["a", "b", "c", "d", "e", "f"], ["b", "d", "f", "h"]))


# B. Первый неповторяющийся символ

def first_unique_char(s):
    hash_table = {}

    # Считаем количество каждого символа
    for char in s:
        hash_table[char] = hash_table.get(char, 0) + 1

    # Ищем первый символ, который встретился один раз
    for char in s:
        if hash_table[char] == 1:
            return char

    return None


print("\nB:")
print(first_unique_char("minimum"))


# C. Длина самого длинного палиндрома

def longest_palindrome(s):
    hash_table = {}

    # Считаем количество каждой буквы
    for char in s:
        hash_table[char] = hash_table.get(char, 0) + 1

    length = 0
    has_odd = False

    # Используем чётные количества символов
    for count in hash_table.values():
        length += (count // 2) * 2

        # Один нечётный символ можно поставить в центр
        if count % 2 == 1:
            has_odd = True

    if has_odd:
        length += 1

    return length


print("\nC:")
test_cases_c = [
    "aAbBABba",
    "abcdefghijklmnoPQrstuvwxyz",
    "wasitacaroracatisaw",
    "bbbabab",
    "abcdeedcba",
    "looooooongestpalindrOme"
]

for s in test_cases_c:
    print(f'"{s}" -> {longest_palindrome(s)}')


# D. Проверка на анаграмму

def is_anagram(s, t):
    # Если длины разные, анаграмм быть не может
    if len(s) != len(t):
        return False

    hash_table = {}

    # Считаем символы первой строки
    for char in s:
        hash_table[char] = hash_table.get(char, 0) + 1

    # Уменьшаем количество символов второй строки
    for char in t:
        if char not in hash_table:
            return False

        hash_table[char] -= 1

        if hash_table[char] < 0:
            return False

    return True


print("\nD:")
test_cases_d = [
    ("нора", "рано"),
    ("монета", "отмена"),
    ("мышка", "камыш"),
    ("тормони", "монитор"),
    ("тоемони", "монитор")
]

for s, t in test_cases_d:
    print(f'"{s}", "{t}" -> {is_anagram(s, t)}')
