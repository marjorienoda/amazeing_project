import random

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
        for h in range(0, self.height):
            row = []
            for w in range(0, self.width):
                current_cell = Cell(w, h)
                row.append(current_cell)
            grid.append(row)
        return grid
    
    def get_unvisited_neighbors(self, current_cell: Cell) -> list[Cell]:
        neighbors: list[Cell] = []
        if current_cell.y - 1 >= 0:
            north_cell = self.grid[current_cell.y - 1][current_cell.x]
            if not north_cell.visited:
                neighbors.append(north_cell)
        if current_cell.y + 1 < self.height:
            south_cell = self.grid[current_cell.y + 1][current_cell.x]
            if not south_cell.visited:
                neighbors.append(south_cell)
        if current_cell.x + 1 < self.width:
            east_cell = self.grid[current_cell.y][current_cell.x + 1]
            if not east_cell.visited:
                neighbors.append(east_cell)
        if current_cell.x - 1 >=  0:
            west_cell = self.grid[current_cell.y][current_cell.x - 1]
            if not west_cell.visited:
                neighbors.append(west_cell)
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
                next_cell = random.choice(neighbors)
                if next_cell.y == current_cell.y - 1:
                    next_cell.walls["south"] = False
                    current_cell.walls["north"] = False
                elif next_cell.y == current_cell.y + 1:
                    next_cell.walls["north"] = False
                    current_cell.walls["south"] = False
                elif next_cell.x == current_cell.x + 1:
                    next_cell.walls["west"] = False
                    current_cell.walls["east"] = False
                elif next_cell.x == current_cell.x - 1:
                    next_cell.walls["east"] = False
                    current_cell.walls["west"] = False
                next_cell.visited = True
                stack.append(next_cell)
            else:
                stack.pop()
