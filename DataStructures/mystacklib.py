from typing import Any, List


class MyStackLib:
    array = []

    def __init__(self, value: Any):
        self.value = value

    def pop(self):
        return self.array[-1]

    def add(self):
        self.array.append(self.value)

    def is_empty(self):
        if len(self.array) == 0:
            return True
        return False
