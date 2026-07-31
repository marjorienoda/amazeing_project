def make_grid(maze: MazeGenerator):
    rows = len(maze.grid)
    cols = len(maze.grid[0])
    new_grid = [
        [" " for _ in range(2 * cols + 1)] for _ in range(2 * rows + 1)
    ]


def main() -> None:
    test = MazeGenerator(
        grid=[[Cell], [9, 5, 6], [12, 5, 7]], entry=(0, 0), exit=(2, 2)
    )
    print(test.grid)
    print(test.entry)
    print(test.exit)

    display(test)


# test
if __name__ == "__main__":
    main()
