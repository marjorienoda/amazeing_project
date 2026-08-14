import random

from display import (
    build_display_grid,
    change_wall_color,
    render,
    show_solve,
)
from generator import MazeGenerator
from make_outputfile import make_output
from read_config import convert_keys, read_config


def main() -> None:
    key_dict = read_config("config.txt")
    converted_keys = convert_keys(key_dict)
    maze = MazeGenerator(**converted_keys)
    maze.generate()

    base_grid = build_display_grid(maze)

    render(base_grid)
    print()
    color = None
    show_path = False
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
        elif selected_mode == "2":
            show_path = not show_path  # 選ぶたびに逆転させる
        elif selected_mode == "3":
            color = input("Color: ")
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
        make_output(maze)


if __name__ == "__main__":
    main()
