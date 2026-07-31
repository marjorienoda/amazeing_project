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


class MazeGenerator:
    def __init__(self, width, height, seed, entry, exit):
        self.width = width
        self.height = height
        self.seed = seed
        self.grid: list[list[Cell]] = []
        self.entry: tuple[int, int] = entry
        self.exit: tuple[int, int] = exit
