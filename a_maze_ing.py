import random

from display import (
    add_start_goal,
    change_wall_color,
    fill_42patern,
    make_grid,
    render,
)
from generator import MazeGenerator
from read_config import convert_keys, read_config


def main() -> None:
    # test_grid = make_test_grid()
    key_dict = read_config("config.txt")
    converted_keys = convert_keys(key_dict)
    maze = MazeGenerator(**converted_keys)
    maze.generate()

    ascii_grid = make_grid(maze)
    final_grid = fill_42patern(maze, add_start_goal(maze, ascii_grid))

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
            new_seed = random.randint(0, 100)
            while new_seed == maze.seed:
                new_seed = random.randint(0, 100)
            maze.seed = new_seed
            maze.generate()
            ascii_grid = make_grid(
                maze
            )  # generateする度にこれもやらないと反映されない→display()みたいなのでまとめる？
            final_grid = fill_42patern(maze, add_start_goal(maze, ascii_grid))
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
            display_grid = change_wall_color(final_grid, color)
            if display_grid is None:
                print("Color change was Failure")
                display_grid = final_grid
        else:
            display_grid = final_grid
        render(display_grid)


if __name__ == "__main__":
    main()
