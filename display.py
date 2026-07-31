class MazeGenerator:
	def __init__(self, width, height, seed, entry, exit):
		self.width = width
		self.height = height
		self.seed = seed
		self.grid: list[list[Cell]] = []
		self.entry: tuple[int, int] = entry
		self.exit: tuple[int, int] = exit
	def generator():
		
		return grid

	def solve():
		self.entry
		self.exit
		if hashdhhd
		else:
				hdifidjfis


class Cell:
    def init(self, x: int, y: int):
        self.x = x
        self.y = y
        self.visited: bool = False
        self.walls: dict[str, bool] = {
            "north": True,
            "south": True,
            "east": True,
            "west": True,
        }

def make_grid(maze: MazeGenerator):
	rows = len(maze.grid)
	cols = len(maze.grid[0])
	new_grid = [[" " for _ in range(2 * cols + 1)] for _ in range(2 * rows + 1)]



def main() -> None:
	test = MazeGenerator(grid=[[Cell], [9, 5, 6], [12, 5, 7]], entry=(0, 0), exit=(2, 2))
	print(test.grid)
	print(test.entry)
	print(test.exit)

	display(test)


#test
if __name__ == "__main__":
	main()

