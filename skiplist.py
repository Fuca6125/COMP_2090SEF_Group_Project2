import random
import bisect
import timeit

class Node:
    def __init__(self, value, level):
        self.value = value
        self.forward = [None] * (level + 1)

class SkipList:
    def __init__(self, max_level=5, p=0.5):
        self.max_level = max_level
        self.p = p
        self.level = 0
        self.header = Node(float('-inf'), max_level)

    def random_level(self):
        lvl = 0
        while random.random() < self.p and lvl < self.max_level:
            lvl += 1
        return lvl

    def insert(self, value):
        update = [None] * (self.max_level + 1)
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].value < value:
                current = current.forward[i]
            update[i] = current
        current = current.forward[0]
        if current is None or current.value != value:
            lvl = self.random_level()
            if lvl > self.level:
                for i in range(self.level + 1, lvl + 1):
                    update[i] = self.header
                self.level = lvl
            new_node = Node(value, lvl)
            for i in range(lvl + 1):
                new_node.forward[i] = update[i].forward[i]
                update[i].forward[i] = new_node

    def search(self, value):
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].value < value:
                current = current.forward[i]
            if current.forward[i] and current.forward[i].value == value:
                return True
        return False


if __name__ == "__main__":
    # Generate random sorted list
    random_list = sorted(random.sample(range(1, 200), 20))
    print("Random sorted list:", random_list)

    # Build skip list
    sl = SkipList(max_level=6)
    for val in random_list:
        sl.insert(val)

    # Search demo
    test_vals = [random.choice(random_list), random.randint(1, 200)]
    for t in test_vals:
        print(f"Searching for {t}:",
              "Found" if sl.search(t) else "Not Found")

    # Performance comparison
    sizes = [1000, 5000, 10000, 50000]
    for n in sizes:
        data = list(range(n))
        skiplist = SkipList(max_level=6)
        for i in data:
            skiplist.insert(i)
        target = random.randint(0, n-1)

        linear_time = timeit.timeit(lambda: target in data, number=1000)
        skip_time = timeit.timeit(lambda: skiplist.search(target), number=1000)
        binary_time = timeit.timeit(lambda: bisect.bisect_left(data, target), number=1000)

        print(f"n={n}: Linear={linear_time:.6f}, SkipList={skip_time:.6f}, Binary={binary_time:.6f}")
