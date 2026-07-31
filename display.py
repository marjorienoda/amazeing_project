from main import Cell, MazeGenerator


def make_grid(maze: MazeGenerator) -> list[list[str]]:
    rows = len(maze.grid)
    cols = len(maze.grid[0])
    new_grid = [
        [" " for _ in range(2 * cols + 1)] for _ in range(2 * rows + 1)
    ]
    ## empty gridを作る

    for row in range(0, 2 * rows + 1, 2):
        for col in range(0, 2 * cols + 1, 2):
            new_grid[row][col] = "+"
    ## 交点（intersection）に　+　を置く

    for row in range(1, 2 * rows + 1, 2):
        for col in range(1, 2 * cols + 1, 2):
            new_grid[row][col] = "   "
    #| と |の間に３マス分スペースを置く

    for row in range(0, 2 * rows + 1, 2):
        for col in range(1, 2 * cols + 1, 2):
            new_grid[row][col] = "   "
    # + と +　の間に3マス分スペースを置く

    # # ここまでで壁のないgridが完成
    #   +   +   +   +

    #   +   +   +   +

    #   +   +   +   +

    #   +   +   +   +

    for y in range(rows):
        for x in range(cols):
            cell = maze.grid[y][x]  # こっちは　3x3の座標だからxとy
            if cell.walls["north"]:
                new_grid[2 * y][2 * x + 1] = "---"  # こっちはASCII gridの座標
            if cell.walls["south"]:
                new_grid[2 * y + 2][2 * x + 1] = "---"
            if cell.walls["east"]:
                new_grid[2 * y + 1][2 * x + 2] = "|"
            if cell.walls["west"]:
                new_grid[2 * y + 1][2 * x] = "|"

    return new_grid


def add_start_goal(
    maze: MazeGenerator, grid: list[list[str]]
) -> list[list[str]]:
    x, y = maze.entry
    grid[2 * y + 1][2 * x + 1] = " S "
    x, y = maze.exit
    grid[2 * y + 1][2 * x + 1] = " G "
    return grid


def make_test_grid():
    cell_1 = Cell(x=0, y=0)
    cell_2 = Cell(x=1, y=0)
    cell_3 = Cell(x=2, y=0)
    cell_1.walls["north"] = True
    cell_1.walls["east"] = False
    cell_1.walls["south"] = True
    cell_1.walls["west"] = True

    cell_2.walls["north"] = True
    cell_2.walls["east"] = False
    cell_2.walls["south"] = True
    cell_2.walls["west"] = False

    cell_3.walls["north"] = True
    cell_3.walls["east"] = True
    cell_3.walls["south"] = False
    cell_3.walls["west"] = False

    cell_4 = Cell(x=0, y=1)
    cell_5 = Cell(x=1, y=1)
    cell_6 = Cell(x=2, y=1)
    cell_4.walls["north"] = True
    cell_4.walls["east"] = False
    cell_4.walls["south"] = False
    cell_4.walls["west"] = True

    cell_5.walls["north"] = True
    cell_5.walls["east"] = False
    cell_5.walls["south"] = True
    cell_5.walls["west"] = False

    cell_6.walls["north"] = False
    cell_6.walls["east"] = True
    cell_6.walls["south"] = True
    cell_6.walls["west"] = False

    cell_7 = Cell(x=0, y=2)
    cell_8 = Cell(x=1, y=2)
    cell_9 = Cell(x=2, y=2)
    cell_7.walls["north"] = False
    cell_7.walls["east"] = False
    cell_7.walls["south"] = True
    cell_7.walls["west"] = True

    cell_8.walls["north"] = True
    cell_8.walls["east"] = False
    cell_8.walls["south"] = True
    cell_8.walls["west"] = False

    cell_9.walls["north"] = True
    cell_9.walls["east"] = True
    cell_9.walls["south"] = True
    cell_9.walls["west"] = False
    grid = [
        [cell_1, cell_2, cell_3],
        [cell_4, cell_5, cell_6],
        [cell_7, cell_8, cell_9],
    ]
    return grid


def main() -> None:

    test_grid = make_test_grid()
    maze = MazeGenerator(width=3, height=3, seed=0, entry=(0, 0), exit=(2, 2))
    maze.grid = test_grid
    grid = make_grid(maze)
    add_SG_grid = add_start_goal(maze, grid)
    new_grid = []
    for i in add_SG_grid:
        new_grid.append("".join(i))
    print("\n".join(new_grid))


if __name__ == "__main__":
    main()
