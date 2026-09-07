import random
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
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        output_file: str,
        perfect: bool = False,
        seed: int | None = None
    ):
        self.width = width
        self.height = height
        self.grid: list[list[Cell]] = []
        self.entry: tuple[int, int] = entry
        self.exit: tuple[int, int] = exit
        self.output_file = output_file
        self.perfect = perfect
        if seed is None:
            self.seed = random.randint(0, 100)
        else:
            self.seed = seed

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

    def get_unvisited_neighbors(
        self, current_cell: Cell
    ) -> list[tuple[Cell, str]]:
        valid_neighbors: list[tuple[Cell, str]] = self.get_valid_neighbors(
            current_cell
        )
        unvisited_neighbors: list[tuple[Cell, str]] = []
        for cell, direction in valid_neighbors:
            if cell.visited is False:
                unvisited_neighbors.append((cell, direction))
        return unvisited_neighbors

    def get_connected_neighbors(
        self, current_cell: Cell, visited_bfs: set[tuple[int, int]]
    ) -> list[tuple[Cell, str]]:
        valid_neighbors: list[tuple[Cell, str]] = self.get_valid_neighbors(
            current_cell
        )
        connected_neighbors: list[tuple[Cell, str]] = []
        for cell, direction in valid_neighbors:
            if (cell.x, cell.y) not in visited_bfs and current_cell.walls[
                direction
            ] is False:
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
            )
        return close_cells

    def close_cells(self, cells_list: list[tuple[int, int]]) -> None:
        for cell_y, cell_x in cells_list:
            cell = self.grid[cell_y][cell_x]
            for direction in cell.walls:
                cell.walls[direction] = True
            for neighbor, direction in self.get_valid_neighbors(cell):
                neighbor.walls[OPPOSITE[direction]] = True
            cell.visited = True

    def get_dead_ends(self) -> list[Cell]:
        dead_ends = []
        for h in range(self.height):
            for w in range(self.width):
                current_cell = self.grid[h][w]
                walls_count = sum(
                    1 for val in current_cell.walls.values() if val is True
                )
                if walls_count == 3:
                    dead_ends.append(current_cell)
        return dead_ends

    def braid(self, pattern_cells: list[tuple[int, int]]) -> None:
        dead_ends = self.get_dead_ends()
        for current_cell in dead_ends:
            list_directions: list[tuple[Cell, str]] = []
            valid_neighbors: list[tuple[Cell, str]] = self.get_valid_neighbors(
                current_cell
            )
            for cell, direction in valid_neighbors:
                if current_cell.walls[direction] is True:
                    if (cell.y, cell.x) in pattern_cells:
                        continue
                    list_directions.append((cell, direction))
            if not list_directions:
                continue
            next_cell, chosen_direction = random.choice(list_directions)
            current_cell.walls[chosen_direction] = False
            next_cell.walls[OPPOSITE[chosen_direction]] = False

    def is_block_fully_connected(self, x: int, y: int) -> bool:
        block_cells: set[tuple[int, int]] = set()
        for row in range(y, y + 3):
            for col in range(x, x + 3):
                block_cells.add((col, row))

        start_cell = self.grid[y][x]
        queue = deque()
        queue.append(start_cell)
        visited: set[tuple[int, int]] = set()
        visited.add((x, y))
        while queue:
            current_cell = queue.popleft()
            connected_neighbors = self.get_connected_neighbors(
                current_cell, visited
            )
            for next_cell, direction in connected_neighbors:
                if (next_cell.x, next_cell.y) in block_cells:
                    visited.add((next_cell.x, next_cell.y))
                    queue.append(next_cell)
        return len(block_cells) == len(visited)

    def fix_large_open_areas(
        self,
    ) -> None:  # インデントが多すぎるので、関数分けるべきかも？
        for row in range(self.height - 2):
            for col in range(self.width - 2):
                if self.is_block_fully_connected(col, row):
                    block_cells: set[tuple[int, int]] = set()
                    candidates: list[tuple[Cell, Cell, str]] = []
                    for r in range(row, row + 3):
                        for c in range(col, col + 3):
                            block_cells.add((c, r))
                            current_cell = self.grid[r][c]
                            valid_neighbors: list[tuple[Cell, str]] = (
                                self.get_valid_neighbors(current_cell)
                            )
                            for cell, direction in valid_neighbors:
                                if (
                                    current_cell.walls[direction] is False
                                    and (cell.x, cell.y) in block_cells
                                ):
                                    candidates.append(
                                        (current_cell, cell, direction)
                                    )
                    while candidates:
                        cell_to_close, neighbor_cell, direction_to_close = (
                            random.choice(candidates)
                        )

                        cell_to_close.walls[direction_to_close] = True
                        neighbor_cell.walls[OPPOSITE[direction_to_close]] = (
                            True
                        )

                        if not self.is_block_fully_connected(col, row):
                            cell_to_close.walls[direction_to_close] = False
                            neighbor_cell.walls[
                                OPPOSITE[direction_to_close]
                            ] = False
                            break
                        else:
                            if not self.is_block_fully_connected(col, row):
                                break
                            candidates.remove(
                                (
                                    cell_to_close,
                                    neighbor_cell,
                                    direction_to_close,
                                )
                            )

    def generate(self) -> None:
        self.grid = self.build_grid()
        close_cell_list = self.calc_42patern()
        entry_yx = (self.entry[1], self.entry[0])
        exit_yx = (self.exit[1], self.exit[0])
        # self.entry/self.exit は (x, y) 順だが、close_cell_list は (y, x) 順
        # （self.grid[y][x] でアクセスするため）なので、↓のifで比較する前に順序を揃える
        if (entry_yx in close_cell_list) or (exit_yx in close_cell_list):
            raise ValueError(
                f"Entry {self.entry} or exit {self.exit} "
                "overlaps with the '42' pattern; "
                "choose different entry/exit coordinates "
                "or a larger maze size."
            )
        else:
            self.close_cells(close_cell_list)
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

        if self.perfect is False:
            self.braid(close_cell_list)

        self.fix_large_open_areas()
        if self.perfect is False:
            self.braid(
                close_cell_list
            )  # これを入れるとdeadendがなくなる fix_large_open_areas()で壁を閉じた→dead_endが作られるかも→braidで消す
        # fix_large_open_areas()で閉じた壁をbraid()が開けてしまう→3x3がまたできてしまうのでは？

    def solve(self) -> str:
        start_cell = self.grid[self.entry[1]][self.entry[0]]
        queue = deque()
        queue.append(start_cell)
        visited_bfs: set[tuple[int, int]] = set()
        visited_bfs.add((start_cell.x, start_cell.y))
        came_from_dic: dict[tuple[int, int], tuple[Cell, str]] = {}

        while queue:
            current_cell = queue.popleft()
            if (
                current_cell.x == self.exit[0]
                and current_cell.y == self.exit[1]
            ):
                break
            else:
                connected_neighbors = self.get_connected_neighbors(
                    current_cell, visited_bfs
                )
                for next_cell, direction in connected_neighbors:
                    visited_bfs.add((next_cell.x, next_cell.y))
                    came_from_dic[(next_cell.x, next_cell.y)] = (
                        current_cell,
                        direction,
                    )
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
        return "".join(path)
