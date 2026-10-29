# Лабораторная работа 6. Деревья

from collections import deque


# Бинарное дерево как структура данных

class TreeNode:
    # Узел дерева: значение и ссылки на левого и правого ребёнка
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class BinaryTree:
    def __init__(self, values):
        # Строим дерево из списка по уровням, None — пустое место
        self.root = self.build(values)

    def build(self, values):
        # Пустой список или пустой корень — дерева нет
        if not values or values[0] is None:
            return None

        root = TreeNode(values[0])
        queue = deque([root])   # узлы, которым ещё нужно присоединить детей
        i = 1                   # индекс следующего значения в списке

        while queue and i < len(values):
            node = queue.popleft()

            # Левый ребёнок
            if i < len(values) and values[i] is not None:
                node.left = TreeNode(values[i])
                queue.append(node.left)
            i += 1

            # Правый ребёнок
            if i < len(values) and values[i] is not None:
                node.right = TreeNode(values[i])
                queue.append(node.right)
            i += 1

        return root


# A. Является ли дерево зеркальным отражением самого себя

def is_symmetric(tree):
    # Проверяем, что два поддерева — зеркальные копии друг друга
    def is_mirror(left, right):
        # Оба пустые — симметрично
        if left is None and right is None:
            return True

        # Только одно пустое — не симметрично
        if left is None or right is None:
            return False

        # Значения должны совпадать, а внешние и внутренние дети — быть зеркальными
        return (left.value == right.value
                and is_mirror(left.left, right.right)
                and is_mirror(left.right, right.left))

    if tree.root is None:
        return True

    return is_mirror(tree.root.left, tree.root.right)


print("A:")
print(is_symmetric(BinaryTree([1, 2, 2, 3, 4, 4, 3])))
print(is_symmetric(BinaryTree([1, 2, 2, None, 3, None, 3])))


# B. Диаметр дерева

def diameter(tree):
    best = 0   # самый длинный путь (в рёбрах), найденный на данный момент

    # Возвращает высоту поддерева (число узлов на самом длинном пути вниз)
    def height(node):
        nonlocal best

        if node is None:
            return 0

        left_height = height(node.left)
        right_height = height(node.right)

        # Самый длинный путь через этот узел = высота слева + высота справа
        best = max(best, left_height + right_height)

        return max(left_height, right_height) + 1

    height(tree.root)
    return best


print("\nB:")
print(diameter(BinaryTree([1, 2, 3, 4, 5])))
print(diameter(BinaryTree([1, 2])))


# C. Являются ли узлы x и y кузенами

def is_cousins(tree, x, y):
    # Ищем глубину и родителя для нужного значения обходом в ширину
    def find(value):
        queue = deque([(tree.root, None, 0)])   # (узел, родитель, глубина)

        while queue:
            node, parent, depth = queue.popleft()
            if node is None:
                continue

            if node.value == value:
                return parent, depth

            queue.append((node.left, node, depth + 1))
            queue.append((node.right, node, depth + 1))

        return None, -1

    parent_x, depth_x = find(x)
    parent_y, depth_y = find(y)

    # Кузены: одинаковая глубина и разные родители
    return depth_x == depth_y and depth_x != -1 and parent_x is not parent_y


print("\nC:")
print(is_cousins(BinaryTree([1, 2, 3, 4]), 4, 3))
print(is_cousins(BinaryTree([1, 2, 3, None, 4, None, 5]), 5, 4))


# D. Есть ли в root поддерево, совпадающее с subRoot

def is_subtree(tree, sub_tree):
    # Проверяем, что два дерева полностью одинаковые
    def same(a, b):
        if a is None and b is None:
            return True
        if a is None or b is None:
            return False

        return a.value == b.value and same(a.left, b.left) and same(a.right, b.right)

    # Пробуем каждый узел root как начало поддерева
    def check(node):
        if node is None:
            return False

        if same(node, sub_tree.root):
            return True

        return check(node.left) or check(node.right)

    return check(tree.root)


print("\nD:")
print(is_subtree(BinaryTree([3, 4, 5, 1, 2]), BinaryTree([4, 1, 2])))
print(is_subtree(BinaryTree([3, 4, 5, 1, 2, None, None, None, None, 0]), BinaryTree([4, 1, 2])))
