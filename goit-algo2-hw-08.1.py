import random
import time


class Node:
    def __init__(self, key, value):
        self.data = (key, value)
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def push(self, key, value):
        node = Node(key, value)
        node.next = self.head
        if self.head:
            self.head.prev = node
        else:
            self.tail = node
        self.head = node
        return node

    def remove(self, node):
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next

        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

        node.prev = None
        node.next = None

    def move_to_front(self, node):
        if node != self.head:
            self.remove(node)
            node.next = self.head
            self.head.prev = node
            self.head = node

    def remove_last(self):
        if self.tail:
            node = self.tail
            self.remove(node)
            return node
        return None


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.list = DoublyLinkedList()

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self.list.move_to_front(node)
            return node.data[1]
        return -1

    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.data = (key, value)
            self.list.move_to_front(node)
        else:
            if len(self.cache) >= self.capacity:
                last = self.list.remove_last()
                if last:
                    del self.cache[last.data[0]]
            node = self.list.push(key, value)
            self.cache[key] = node


# 1. Усі функції: range_sum_no_cache, update_no_cache — реалізовані та працюють.
# Без кешу
def range_sum_no_cache(array, left, right):
    return sum(array[left:right + 1])


def update_no_cache(array, index, value):
    array[index] = value


# 1. Усі функції: range_sum_with_cache, update_with_cache — реалізовані та працюють.
# З кешем
cache = LRUCache(capacity=1000)

def range_sum_with_cache(array, left, right):
    key = (left, right)
    cached = cache.get(key)
    if cached != -1:
        return cached

    result = sum(array[left:right + 1])
    cache.put(key, result)
    return result


def update_with_cache(array, index, value):
    array[index] = value

    keys_to_remove = []
    for (l, r) in cache.cache.keys():
        if l <= index <= r:
            keys_to_remove.append((l, r))

    for key in keys_to_remove:
        node = cache.cache[key]
        cache.list.remove(node)
        del cache.cache[key]


# Функція для тестування із ТЗ
def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):
    hot = [(random.randint(0, n // 2), random.randint(n // 2, n - 1))
           for _ in range(hot_pool)]
    queries = []

    for _ in range(q):
        if random.random() < p_update:
            idx = random.randint(0, n - 1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))
        else:
            if random.random() < p_hot:
                left, right = random.choice(hot)
            else:
                left = random.randint(0, n - 1)
                right = random.randint(left, n - 1)
            queries.append(("Range", left, right))

    return queries


# 2. Програма вимірює час виконання запитів з кешем і без нього та виводить результати у зрозумілому вигляді.
if __name__ == "__main__":
    N = 100_000
    Q = 50_000

    array = [random.randint(1, 100) for _ in range(N)]
    queries = make_queries(N, Q)

    # Без кешу
    start_no_cache = time.time()
    for q in queries:
        if q[0] == "Range":
            range_sum_no_cache(array, q[1], q[2])
        else:
            update_no_cache(array, q[1], q[2])
    end_no_cache = time.time()

    time_no_cache = end_no_cache - start_no_cache

    # З кешем
    array = [random.randint(1, 100) for _ in range(N)]
    cache = LRUCache(capacity=1000)

    start_cache = time.time()
    for q in queries:
        if q[0] == "Range":
            range_sum_with_cache(array, q[1], q[2])
        else:
            update_with_cache(array, q[1], q[2])
    end_cache = time.time()

    time_cache = end_cache - start_cache



# 3. Результати тестування представлені у зручному для розуміння форматі, щоб можна було оцінити ефективність використання LRU-кешу.
    print("\nРезультати тестування продуктивності:")
    print(f"Без кешу : {time_no_cache:.2f} c")
    print(f"LRU-кеш  : {time_cache:.2f} c  (прискорення ×{time_no_cache / time_cache:.1f})")

















