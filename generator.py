import random

OPPOSITE = {
    "north": "south",
    "east": "west",
    "south": "north",
    "west": "east",
}  # 変わらないものだから、定数として扱いたい


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
    def __init__(self, width, height, seed, entry, exit, perfect=False):
        self.width = width
        self.height = height
        self.seed = seed
        self.grid: list[list[Cell]] = []
        self.entry: tuple[int, int] = entry
        self.exit: tuple[int, int] = exit
        self.perfect = perfect

    def build_grid(self) -> list[list[Cell]]:
        grid = []
        for h in range(self.height):
            row = []
            for w in range(self.width):
                current_cell = Cell(w, h)
                row.append(current_cell)
            grid.append(row)
        return grid
    
    def get_unvisited_neighbors(self, current_cell: Cell) -> list[tuple[Cell, str]]:
        neighbors: list[tuple[Cell, str]] = []
        north_cell = (current_cell.y - 1, current_cell.x)
        east_cell = (current_cell.y, current_cell.x + 1)
        south_cell = (current_cell.y + 1, current_cell.x)
        west_cell = (current_cell.y, current_cell.x - 1)
        list_direction: list[tuple[tuple[int, int], str]] = [
            (north_cell, "north"),
            (east_cell, "east"),
            (south_cell, "south"),
            (west_cell, "west"),
        ]  # ループする度にリストを作ってるからあまり良くないかも、リストは外で作って値をループで更新する？
        for coordinate, direction in list_direction:
            y, x = coordinate
            if (
                x >= 0 and y >= 0 and x < self.width and y < self.height
            ):  # limit_check
                direction_cell = self.grid[y][x]
                if direction_cell.visited is False:
                    neighbors.append((direction_cell, direction))
        return neighbors

    def generate(self) -> None:
        self.grid = self.build_grid()
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
