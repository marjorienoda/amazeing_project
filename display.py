from generator import MazeGenerator

DIRECTION_DELTA = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}

color_dict: dict[str, str] = {
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
}


def build_display_grid(maze: MazeGenerator) -> list[list[str]]:
    ascii_grid = make_grid(maze)
    base_grid = fill_42patern(maze, add_start_goal(maze, ascii_grid))
    return base_grid


def to_grid_coord(x: int, y: int) -> tuple[int, int]:
    grid_y = 2 * y + 1
    grid_x = 2 * x + 1
    return (grid_y, grid_x)


def make_grid(maze: MazeGenerator) -> list[list[str]]:
    rows = len(maze.grid)
    cols = len(maze.grid[0])
    new_grid = [
        [" " for _ in range(2 * cols + 1)] for _ in range(2 * rows + 1)
    ]  # fill space

    # 交点（intersection）に　+　を置く
    for row in range(0, 2 * rows + 1, 2):
        for col in range(0, 2 * cols + 1, 2):
            new_grid[row][col] = "+"

    # |と|の間に３スペースを置く
    for row in range(1, 2 * rows + 1, 2):
        for col in range(1, 2 * cols + 1, 2):
            new_grid[row][col] = "   "

    # + と +　の間に3スペースを置く
    for row in range(0, 2 * rows + 1, 2):
        for col in range(1, 2 * cols + 1, 2):
            new_grid[row][col] = "   "

    #  ↓ここまでで壁のない No_wall_gridが完成
    #   +   +   +   +

    #   +   +   +   +

    #   +   +   +   +

    #   +   +   +   +

    for y in range(rows):
        for x in range(cols):
            cell = maze.grid[y][
                x
            ]  # こっちは3x3の座標だからxとy　row(行)=y col(列)=y
            if cell.walls["north"]:
                new_grid[2 * y][2 * x + 1] = "---"  # こっちはASCII_gridの座標
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


def fill_42patern(
    maze: MazeGenerator, grid: list[list[str]]
) -> list[list[str]]:
    for y, row in enumerate(maze.grid):
        for x, cell in enumerate(row):
            if all(cell.walls.values()):
                grid[2 * y + 1][2 * x + 1] = "\033[95m" + " # " + "\033[0m"
    return grid


def change_wall_color(
    grid: list[list[str]], color: str
) -> list[list[str]] | None:
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


def show_solve(
    path: str, maze: MazeGenerator, grid: list[list[str]]
) -> list[list[str]]:
    solve_grid: list[list[str]] = []  # show/hideで切り替えるために直接上書きせず、新しいgridをつくる
    for row in grid:  # gridの内容をコピーするためにループしてる
        solve_grid.append(list(row))
    current_x, current_y = maze.entry
    for direction in path:  # "ESNWE..."から1文字を取り出す
        delta_y, delta_x = DIRECTION_DELTA[direction]
        next_x = current_x + delta_x
        next_y = current_y + delta_y
        next_grid_y, next_grid_x = to_grid_coord(next_x, next_y)
        if (next_x, next_y) != maze.exit:
            solve_grid[next_grid_y][next_grid_x] = (
                "\033[96m" + " * " + "\033[0m"
            )
        current_grid_y, current_grid_x = to_grid_coord(current_x, current_y)
        wall_grid_y = (current_grid_y + next_grid_y) // 2
        wall_grid_x = (current_grid_x + next_grid_x) // 2
        if direction == "E" or direction == "W":
            solve_grid[wall_grid_y][wall_grid_x] = "\033[96m" + "*" + "\033[0m"
        else:
            solve_grid[wall_grid_y][wall_grid_x] = (
                "\033[96m" + " * " + "\033[0m"
            )
        current_x, current_y = next_x, next_y
    return solve_grid


def render(display_grid: list[list[str]]) -> None:
    new_grid = []
    for i in display_grid:
        new_grid.append("".join(i))
    print("\n".join(new_grid))
