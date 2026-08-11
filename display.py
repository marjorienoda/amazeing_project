from generator import MazeGenerator


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


# def main() -> None:
#     # test_grid = make_test_grid()
#     maze = MazeGenerator(width=3, height=3, seed=42, entry=(0, 0), exit=(2, 2))
#     maze.generate()

#     ascii_grid = make_grid(maze)
#     final_grid = add_start_goal(maze, ascii_grid)
#     render(final_grid)
#     print()
#     color = None
#     while True:
#         print("=== A-Maze-ing ===")
#         print("1. Re-generate a new maze")
#         print("2. Show / Hide the shortest path")
#         print("3. Rotate the wall colours")
#         print("4. Quit")
#         selected_mode = input("Choice? (1-4): ")
#         if selected_mode == "1":
#             print(1)
#         elif selected_mode == "2":
#             print(2)
#         elif selected_mode == "3":
#             color = input("Color: ")
#         elif selected_mode == "4":
#             print("=== System closed ===")
#             break
#         else:
#             print("No mode")
#         if color:
#             display_grid = change_wall_color(final_grid, color)
#             if display_grid is None:
#                 print("Color change was Failure")
#                 display_grid = final_grid
#         else:
#             display_grid = final_grid
#         render(display_grid)


# if __name__ == "__main__":
#     main()
