from binascii import Error
import dataclasses
from typing import Optional


@dataclasses.dataclass
class Vector2D:
    x: float | int
    y: float | int

    @staticmethod
    def zero() -> "Vector2D":
        return Vector2D(0, 0)
    
    def __add__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(
            self.x + other.x,
            self.y + other.y,
        )
    
    def __mul__(self, other: int | float) -> "Vector2D":
        return Vector2D(
            self.x * other,
            self.y * other,
        )
    
    def __truediv__(self, other: int | float) -> "Vector2D":
        return Vector2D(
            self.x / other,
            self.y / other,
        )


@dataclasses.dataclass
class Node:
    mass: float
    center_mass: Vector2D

    @staticmethod
    def empty() -> "Node":
        return Node(0, Vector2D.zero())
    
    def is_empty(self) -> bool:
        return self.mass == 0
    
    def add_mass(self, position: Vector2D, mass: float) -> None:
        self.center_mass = ((self.center_mass * self.mass) + (position * mass)) / (self.mass + mass)
        self.mass += mass


class QuadTree:
    def __init__(
        self,
        size: float,
        offset: Optional[Vector2D] = None,
    ):
        self.nodes: list[Optional[Node]] = [None]
        self.tree: list[Optional[tuple[int, int, int, int]]] = [None]
        self.size = size
        self.offset = offset if offset is not None else Vector2D.zero()

    def add(self, position: Vector2D, mass: float, max_recursion_fallback: int = 10_000) -> None:
        recursion = -1
        
        current_node_index = 0
        current_size = self.size
        current_start_position = self.offset

        while recursion <= max_recursion_fallback:
            recursion += 1

            current_node = self.nodes[current_node_index]
            current_tree_section = self.tree[current_node_index]

            if current_node is None:
                self.nodes[current_node_index] = Node(mass, position)
                return

            if current_tree_section is None:
                child_nodes = [None] * 4
                pass_child_current_node_index = self._position_to_index(current_node.center_mass, current_start_position, current_size)
                child_nodes[pass_child_current_node_index] = Node(current_node.mass, current_node.center_mass)
                self.nodes.extend(child_nodes)

                self.tree.extend(None for i in range(4))
                self.tree[current_node_index] = current_tree_section = (len(self.nodes) - 4, len(self.nodes) - 3, len(self.nodes) - 2, len(self.nodes) - 1)
            
            current_node.add_mass(position, mass)

            next_index_offset = self._position_to_index(position, current_start_position, current_size)

            current_node_index += next_index_offset + 1
            current_size /= 2
            current_start_position += (self._index_to_relative_normalized_position(next_index_offset) * current_size)
        
        raise Error(f"Recursion searching reach max value, {max_recursion_fallback}")

    @staticmethod
    def _position_to_index(
        position: Vector2D,
        referential_origin_position: Vector2D,
        referential_size: float,
    ) -> int:
        """
        Disposition will be like this
        -----
        |0|1|
        |2|3|
        -----
        """
        half_referential = referential_origin_position + (Vector2D(1, 1) * referential_size / 2)
        if position.x < half_referential.x and position.y < half_referential.y:
            return 0
        if position.x >= half_referential.x and position.y >= half_referential.y:
            return 3
        if position.x < half_referential.x:
            return 2
        if position.x >= half_referential.x:
            return 1
        raise Error(f"Unable to convert the position into index from this configuration, {position=}, {referential_origin_position=}, {referential_size=}")
    
    @staticmethod
    def _index_to_relative_normalized_position(index: int) -> Vector2D:        
        match index:
            case 0:
                return Vector2D(0, 0)
            case 1:
                return Vector2D(1, 0)
            case 2:
                return Vector2D(0, 1)
            case 3:
                return Vector2D(1, 1)
            case _:
                raise Error(f"Index out of range, {index} must be between 0 and 3")
    
    def _tree_str(self) -> str:
        """Return a tree representation of the quadtree."""

        def visit(node: int, prefix: str, name: str, is_last: bool) -> list[str]:
            branch = "└── " if is_last else "├── "
            lines = [f"{prefix}{branch}{name}"]

            children = self.tree[node]
            if children is None:
                return lines

            next_prefix = prefix + ("    " if is_last else "│   ")

            labels = ("NW", "NE", "SW", "SE")
            for i, child in enumerate(children):
                last = i == 3
                if child is None:
                    lines.append(
                        f"{next_prefix}{'└── ' if last else '├── '}{labels[i]} [leaf]"
                    )
                else:
                    lines.extend(visit(child, next_prefix, labels[i], last))

            return lines

        return "\n".join(["□", *visit(0, "", "ROOT", True)[1:]])
    
    def _grid_str(self, width: int = 64, height: int = 32) -> str:
        """Return an ASCII drawing of the spatial subdivision."""

        canvas = [[" " for _ in range(width)] for _ in range(height)]

        def hline(y, x0, x1):
            for x in range(x0, x1):
                canvas[y][x] = "-"

        def vline(x, y0, y1):
            for y in range(y0, y1):
                canvas[y][x] = "|"

        def recurse(node, x, y, w, h):
            children = self.tree[node]
            if children is None:
                return

            mx = x + w // 2
            my = y + h // 2

            vline(mx, y, y + h)
            hline(my, x, x + w)
            canvas[my][mx] = "+"

            quads = [
                (children[0], x, y, w // 2, h // 2),            # NW
                (children[1], mx, y, w - w // 2, h // 2),       # NE
                (children[2], x, my, w // 2, h - h // 2),       # SW
                (children[3], mx, my, w - w // 2, h - h // 2),  # SE
            ]

            for child, cx, cy, cw, ch in quads:
                if child is not None:
                    recurse(child, cx, cy, cw, ch)

        recurse(0, 0, 0, width, height)

        top = "+" + "-" * width + "+"
        bottom = top
        body = ["|" + "".join(row) + "|" for row in canvas]

        return "\n".join([top, *body, bottom])
