import random
import sys
from collections import deque

OPPOSITE = {
    "north": "south",
    "east": "west",
    "south": "north",
    "west": "east",
}  # 変わらないものだから、定数として扱いたい

DIRECTION_LETTERS = {
    "north": "N",
    "east": "E",
    "south": "S",
    "west": "W",
}

class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.visited: bool = False
        self.walls: dict[str, bool] = {
            "north": True,
            "south": True,
            "east": True,
            "west": True,
        }

    def __str__(self):
        return f"x= {self.x}, y={self.y} "


class MazeGenerator:
    def __init__(
        self, width, height, seed, entry, exit, output_file, perfect=False
    ):
        self.width = width
        self.height = height
        self.seed = seed
        self.grid: list[list[Cell]] = []
        self.entry: tuple[int, int] = entry
        self.exit: tuple[int, int] = exit
        self.perfect = perfect
        self.output_file = output_file

    def build_grid(self) -> list[list[Cell]]:
        grid = []
        for h in range(self.height):
            row = []
            for w in range(self.width):
                current_cell = Cell(w, h)
                row.append(current_cell)
            grid.append(row)
        return grid

    def get_valid_neighbors(
        self, current_cell: Cell
    ) -> list[tuple[Cell, str]]:
        valid_neighbors: list[tuple[Cell, str]] = []
        north_cell = (current_cell.y - 1, current_cell.x)
        east_cell = (current_cell.y, current_cell.x + 1)
        south_cell = (current_cell.y + 1, current_cell.x)
        west_cell = (current_cell.y, current_cell.x - 1)
        list_direction: list[tuple[tuple[int, int], str]] = [
            (north_cell, "north"),
            (east_cell, "east"),
            (south_cell, "south"),
            (west_cell, "west"),
        ]
        for coordinate, direction in list_direction:
            y, x = coordinate
            if (
                x >= 0 and y >= 0 and x < self.width and y < self.height
            ):  # limit_check
                direction_cell = self.grid[y][x]
                valid_neighbors.append((direction_cell, direction))
        return valid_neighbors
    
    def get_unvisited_neighbors(self, current_cell: Cell) -> list[tuple[Cell, str]]:
        valid_neighbors: list[tuple[Cell, str]] = self.get_valid_neighbors(current_cell)
        unvisited_neighbors: list[tuple[Cell, str]] = []
        for cell, direction in valid_neighbors:
            if cell.visited is False:
                unvisited_neighbors.append((cell, direction))
        return unvisited_neighbors

    def get_connected_neighbors(
        self, current_cell: Cell, visited_bfs: set[tuple[int, int]]
    ) -> list[tuple[Cell, str]]:
        valid_neighbors: list[tuple[Cell, str]] = self.get_valid_neighbors(current_cell)
        connected_neighbors: list[tuple[Cell, str]] = []
        for cell, direction in valid_neighbors:
            if (cell.x, cell.y) not in visited_bfs and current_cell.walls[direction] is False:
                connected_neighbors.append((cell, direction))
        return connected_neighbors

    def calc_42patern(self) -> list[tuple[int, int]]:
        patern_height = 5
        patern_width = 7
        patern_42 = ["1000111", "1000001", "1110111", "0010100", "0010111"]
        center_y, center_x = (
            self.height // 2,
            self.width // 2,
        )  # //にすれば、整数だけになる（小数切り捨て)
        close_cells: list[tuple[int, int]] = []
        if self.width >= patern_width + 2 and self.height >= patern_height + 2:
            start_y = center_y - (patern_height // 2)
            start_x = center_x - (patern_width // 2)
            for y_index, row in enumerate(patern_42):
                for x_index, bit in enumerate(row):
                    if bit == "1":
                        close_cells.append(
                            (start_y + y_index, start_x + x_index)
                        )
        else:
            raise ValueError(
                f"42 pattern requires width >= {patern_width + 2},"
                f" and height >= {patern_height + 2}.",
                f"Current: width={self.width}, height={self.height}",
                file=sys.stderr,
            )
        return close_cells

    def close_cells(self, cells_list: list[tuple[int, int]]) -> None:
        for cell_y, cell_x in cells_list:
            cell = self.grid[cell_y][cell_x]
            for direction in cell.walls:
                cell.walls[direction] = True
            cell.visited = True
    
    def generate(self) -> None:
        self.grid = self.build_grid()
        close_cell_list = self.calc_42patern()
        if not (self.entry in close_cell_list) or (
            self.exit in close_cell_list
        ):
            self.close_cells(close_cell_list)
        else:
            raise ValueError("input error", file=sys.stderr)
        random.seed(self.seed)
        stack: list[Cell] = []
        start_cell = self.grid[self.entry[1]][self.entry[0]]
        start_cell.visited = True
        stack.append(start_cell)
        while stack:
            current_cell = stack[-1]
            neighbors = self.get_unvisited_neighbors(current_cell)
            if neighbors:
                next_cell, direction = random.choice(neighbors)
                current_cell.walls[direction] = False
                next_cell.walls[OPPOSITE[direction]] = False
                # 壁を壊す（２つのセル(current_cell , next_cell)の壁情報を変えないといけない。どの方向を壊すか→direction　next_cellは反対の方向になるのでOPPOSITE[direction]
                next_cell.visited = True
                stack.append(next_cell)
            else:
                stack.pop()
    
    
    def solve(self) -> str:
        start_cell = self.grid[self.entry[1]][self.entry[0]]
        queue = deque()
        queue.append(start_cell)
        visited_bfs: set[tuple[int, int]] = set()
        visited_bfs.add((start_cell.x, start_cell.y))
        came_from_dic: dict[tuple[int, int], tuple[Cell, str]] = {}

        while queue:
            current_cell = queue.popleft()
            if current_cell.x == self.exit[0] and current_cell.y == self.exit[1]:
                break
            else:
                connected_neighbors = self.get_connected_neighbors(current_cell, visited_bfs)
                for next_cell, direction in connected_neighbors:
                    visited_bfs.add((next_cell.x, next_cell.y))
                    came_from_dic[(next_cell.x, next_cell.y)] = (current_cell, direction)
                    queue.append(next_cell)
        
        path: list[str] = []
        current = (self.exit[0], self.exit[1])
        entry_cell = (self.entry[0], self.entry[1])
        while current != entry_cell:
            prev_cell, direction = came_from_dic[current]
            letter = DIRECTION_LETTERS[direction]
            path.append(letter)
            current = (prev_cell.x, prev_cell.y)
        path.reverse()
        return(f"".join(path))
        