import random

from display import add_start_goal, make_grid, render
from maze_generator import Cell, MazeGenerator
from read_config import convert_keys, read_config

OPPOSITE = {
    "north": "south",
    "east": "west",
    "south": "north",
    "west": "east",
}  # 変わらないものだから、定数として扱いたい


def main() -> None:
    key_dict = read_config("config.txt")
    if key_dict is None:
        return

    print("=== read_config ===")
    print(key_dict)

    keys = convert_keys(key_dict)
    if keys is None:
        return

    print("=== convert_keys ===")
    print(keys)

    output_file_name = keys.pop("output_file")

    maze = MazeGenerator(
        **keys
    )  # こうするとまとめて渡せるみたい pythonの*はポインタじゃない
    print(maze.entry)  # sample
    print(output_file_name)  # sample

    maze.grid = []
    for y in range(maze.height):
        row: list[Cell] = []
        for x in range(maze.width):
            row.append(Cell(x, y))
        maze.grid.append(row)
    # print(maze.grid[0][0].walls)  #test_code
    # print(len(maze.grid), len(maze.grid[0])) #test_code
    stack: list[Cell] = []
    current_x, current_y = maze.entry
    current_cell = maze.grid[current_y][current_x]  # get_start_Cell()
    current_cell.visited = True
    stack.append(current_cell)
    random.seed(maze.seed)
    # ここまでがDFSする前の設定

    while stack:
        current_cell = stack[-1]
        # stack[len(stack) - 1]と同じ stack[0]だと前からになる→１番新しいのは末尾stack[-1]
        can_move: list[tuple[Cell, str]] = []  # 動くことができる方向のリスト
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
                x >= 0 and y >= 0 and x < maze.width and y < maze.height
            ):  # limit_check
                direction_cell = maze.grid[y][x]
                if direction_cell.visited is False:
                    can_move.append((direction_cell, direction))
        # ここまでがCheck

        # ここからはCheckで作ったcan_moveからランダムで選んで壁を壊す作業
        if can_move:
            next_cell, direction = random.choice(can_move)
            current_cell.walls[direction] = False
            next_cell.walls[OPPOSITE[direction]] = False
            # 壁を壊す（２つのセル(current_cell , next_cell)の壁情報を変えないといけない。どの方向を壊すか→direction　next_cellは反対の方向になるのでOPPOSITE[direction]
            # Your generated data must be coherent: each neighbouring cell must have the same wall if any. E.g., it is forbidden to have a first cell with a wall on the east side, and the second cell behind that wall without a wall on the west side.
            next_cell.visited = True
            stack.append(next_cell)
        else:
            stack.pop()
    grid = make_grid(maze)
    default_grid = add_start_goal(maze, grid)
    render(default_grid)
    print()


if __name__ == "__main__":
    main()
