import random
import sys

from display import (
    build_display_grid,
    change_wall_color,
    render,
    show_solve,
    color_dict
)
from generator import MazeGenerator
from make_outputfile import make_output
from read_config import (
    check_required_keys,
    convert_keys,
    read_config,
    validate_entry_exit,
    ConfigError
)


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Error: missing config file argument. "
            "Usage: python3 a_maze_ing.py <config_file>",
            file=sys.stderr
        )
        sys.exit(1)
    try:
        key_dict = read_config(sys.argv[1])
        check_required_keys(key_dict)
        converted_keys = convert_keys(key_dict)
        validate_entry_exit(
            converted_keys["width"],
            converted_keys["height"],
            converted_keys["entry"],
            converted_keys["exit"]
        )
    except ConfigError as e:
        print(f"Config error: {e}", file=sys.stderr)
        sys.exit(1)
    try:
        maze = MazeGenerator(**converted_keys)
    except TypeError as e:
        print(f"Missing or invalid key(s) in config.txt: {e}", file=sys.stderr)
        sys.exit(1)
    try:
        maze.generate()
    except ValueError as e:
        print(f"Can not make maze: {e}", file=sys.stderr)
        sys.exit(1)

    base_grid = build_display_grid(maze)

    render(base_grid)
    make_output(maze)
    print()
    color = None
    show_path = False
    color_index = 0
    color_list = [None] + list(color_dict.keys())
     #先頭にNoneを追加したcolor_dictのkeys(red, green, yellow, blue)のlistをcolor_listとする

    while True:
        print("=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show / Hide the shortest path")
        print("3. Rotate the wall colours")
        print("4. Quit")
        selected_mode = input("Choice? (1-4): ")
        if selected_mode == "1":
            new_seed = random.randint(0, 100)
            while new_seed == maze.seed:
                new_seed = random.randint(0, 100)
            maze.seed = new_seed
            maze.generate()
            base_grid = build_display_grid(maze)
            make_output(maze)
            # Mode1: Regenerate = maze.txt was changed → make_output is needed
        elif selected_mode == "2":
            show_path = not show_path  # 選ぶたびに逆転させる
        elif selected_mode == "3":
            color_index += 1
            color = color_list[color_index % len(color_list)]
             #None→Red→Green→Yellow→Blue→NoneとRotateする
        elif selected_mode == "4":
            print("=== System closed ===")
            break
        else:
            print("No mode")
        if color:
            display_grid = change_wall_color(base_grid, color)
            if display_grid is None:
                print("Color change was Failure")
                display_grid = base_grid
        else:
            display_grid = base_grid

        if show_path:
            display_grid = show_solve(maze.solve(), maze, display_grid)
        render(display_grid)


if __name__ == "__main__":
    main()
