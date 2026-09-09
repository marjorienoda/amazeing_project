import sys

from mazegen import MazeGenerator

WALL_BIT = {"north": 0, "east": 1, "south": 2, "west": 3}


def calc_wall_sum(walls_dict: dict[str, bool]) -> int:
    result = 0
    for wall, is_close in walls_dict.items():
        if is_close:
            result += 1 << WALL_BIT[wall]
    return result


def convert_hex(num: int) -> str:
    return hex(num).replace("0x", "")


def make_output(maze: MazeGenerator) -> None:
    output = []
    for cells_list in maze.grid:
        row = []
        for cell in cells_list:
            row.append(convert_hex(calc_wall_sum(cell.walls)))
        row.append("\n")
        output.append("".join(row))
    data = "".join(output) + "\n"
    x, y = maze.entry
    data += f"{x},{y}       #entry  (x,y)\n"
    x, y = maze.exit
    data += f"{x},{y}       #exit   (x,y)\n"
    data += maze.solve() + "\n"
    try:
        with open(maze.output_file, "w") as f:
            f.write(data)
    except OSError as e:
        print(f"{e}", file=sys.stderr)
