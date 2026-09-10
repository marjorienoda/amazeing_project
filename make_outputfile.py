"""Output file writer.

Encodes a generated maze's walls as one hexadecimal digit per cell and
writes it to a file, followed by the entry/exit coordinates and the
solved path, as required by the project's output file format.
"""

import sys

from mazegen import MazeGenerator

WALL_BIT = {"north": 0, "east": 1, "south": 2, "west": 3}


def calc_wall_sum(walls_dict: dict[str, bool]) -> int:
    """Encode a cell's walls as a single integer using bit flags.

    Each closed wall sets its corresponding bit, as defined by
    `WALL_BIT` (north=0, east=1, south=2, west=3). An open wall leaves
    its bit unset.

    Args:
        walls_dict: A cell's walls dictionary, e.g.
            `{"north": True, "south": False, "east": False, "west": True}`.

    Returns:
        An integer between 0 and 15 representing which walls are
        closed.
    """
    result = 0
    for wall, is_close in walls_dict.items():
        if is_close:
            result += 1 << WALL_BIT[wall]
    return result


def convert_hex(num: int) -> str:
    """Convert an integer to its hexadecimal string representation.

    Args:
        num: The integer to convert (expected to be between 0 and 15,
            i.e. a single hex digit).

    Returns:
        The hexadecimal representation of `num`, without the `0x`
        prefix (e.g. `10` becomes `"a"`).
    """
    return hex(num).replace("0x", "")


def make_output(maze: MazeGenerator, output_file: str) -> None:
    """Write the generated maze to the output file.

    The file format is: one hex digit per cell, one row per line,
    followed by a blank line, then the entry coordinates, the exit
    coordinates, and the solved path (as a string of direction
    letters), each on its own line.

    Args:
        maze: The generated maze to write. `maze.generate()` must
            already have been called.
        output_file: Path to the file to write the output to.

    Raises:
        None directly; if the file cannot be written, the error is
        printed to stderr and the function returns normally.
    """
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
        with open(output_file, "w") as f:
            f.write(data)
    except OSError as e:
        print(f"{e}", file=sys.stderr)
