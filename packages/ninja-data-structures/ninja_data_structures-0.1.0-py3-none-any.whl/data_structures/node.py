from typing import Any


class Node:
    def __init__(self, data: Any, next: "Node" = None, prev: "Node" = None) -> None:
        self.data = data
        self.next = next
        self.prev = prev

    def __repr__(self) -> str:
        return f"Node({self.data!r}, {self.next!r}, {self.prev!r})"
