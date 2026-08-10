
from generator import Cell, MazeGenerator


def make_grid(maze: MazeGenerator) -> list[list[str]]:
    rows = len(maze.grid)
    cols = len(maze.grid[0])
    new_grid = [
        [" " for _ in range(2 * cols + 1)] for _ in range(2 * rows + 1)
    ]
    ## fill space

    for row in range(0, 2 * rows + 1, 2):
        for col in range(0, 2 * cols + 1, 2):
            new_grid[row][col] = "+"
    ## 交点（intersection）に　+　を置く

    for row in range(1, 2 * rows + 1, 2):
        for col in range(1, 2 * cols + 1, 2):
            new_grid[row][col] = "   "
    #| と |の間に３スペースを置く

    for row in range(0, 2 * rows + 1, 2):
        for col in range(1, 2 * cols + 1, 2):
            new_grid[row][col] = "   "
    # + と +　の間に3スペースを置く

    #  ↓ここまでで壁のない No_wall_gridが完成
    #   +   +   +   +

    #   +   +   +   +

    #   +   +   +   +

    #   +   +   +   +

    for y in range(rows):
        for x in range(cols):
            cell = maze.grid[y][x]#こっちは3x3の座標だからxとy　row(行)=y col(列)=y
            if cell.walls["north"]:
                new_grid[2 * y][2 * x + 1] = "---"  #こっちはASCII_gridの座標
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


def make_test_grid() -> list[list[Cell]]:
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


def change_wall_color(
    grid: list[list[str]], color: str
) -> list[list[str]] | None:
    color_dict: dict[str, str] = {
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
    }
    try:
        color_code = color_dict[color]
    except KeyError as e:
        print(f"That color is not available. : {e}")
        return None

    colored_grid = []
    for i in grid:
        colored_row = []
        for cell_str in i:
            if "-" in cell_str or "+" in cell_str or "|" in cell_str:
                colored_cell = color_code + cell_str + "\033[0m"
                colored_row.append(colored_cell)
            else:
                colored_row.append(cell_str)
        colored_grid.append(colored_row)
    return colored_grid


def render(display_grid: list[list[str]]) -> None:
    new_grid = []
    for i in display_grid:
        new_grid.append("".join(i))
    print("\n".join(new_grid))


def main() -> None:
    # test_grid = make_test_grid()
    maze = MazeGenerator(width=5, height=5, seed=42, entry=(0,0), exit=(4,4))
    maze.generate()

    ascii_grid = make_grid(maze)
    final_grid = add_start_goal(maze, ascii_grid)
    render(final_grid)
    print()
    color = None
    while True:
        print("=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show / Hide the shortest path")
        print("3. Rotate the wall colours")
        print("4. Quit")
        selected_mode = input("Choice? (1-4): ")
        if selected_mode == "1":
            print(1)
        elif selected_mode == "2":
            print(2)
        elif selected_mode == "3":
            color = input("Color: ")
        elif selected_mode == "4":
            print("=== System closed ===")
            break
        else:
            print("No mode")
        if color:
            display_grid = change_wall_color(default_grid, color)
            if display_grid is None:
                print("Color change was Failure")
                display_grid = default_grid
        else:
            display_grid = default_grid
        render(display_grid)


if __name__ == "__main__":
    main()
