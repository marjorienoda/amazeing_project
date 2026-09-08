*This project has been created as part of the 42 curriculum by mnoda-ta, rkato.*

# mazegen

A reusable maze generation and solving library, implementing a recursive
backtracker (perfect maze generation), an optional braiding pass (loop
generation for non-perfect mazes), and a BFS-based shortest-path solver.

This module was originally built as part of the A-Maze-ing project, but is
designed to be imported and reused independently in other projects.

## Installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

(or build it yourself from source — see the main project's README for
build instructions)

## Basic usage

```python
from mazegen import MazeGenerator

maze = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(19, 14),
    perfect=True,
    seed=42
)
maze.generate()
```

After calling `.generate()`, the maze is fully built and stored on the
`maze` object, ready to be inspected or solved.

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `width` | `int` | yes | Number of columns in the maze |
| `height` | `int` | yes | Number of rows in the maze |
| `entry` | `tuple[int, int]` | yes | Starting coordinates `(x, y)` |
| `exit` | `tuple[int, int]` | yes | Ending coordinates `(x, y)` |
| `perfect` | `bool` | no (default `False`) | If `True`, generates a perfect maze (single path, no loops). If `False`, applies braiding to add loops and reduce dead-ends |
| `seed` | `int` | no (default: random) | Seed for reproducible generation — the same seed and parameters always produce the same maze |

## Accessing the generated structure

The maze is stored as a 2D grid of `Cell` objects, accessed as
`maze.grid[y][x]`. Each `Cell` exposes its coordinates and which of its
four walls are closed:

```python
cell = maze.grid[0][0]
print(cell.x, cell.y)          # 0 0
print(cell.walls)              # {'north': True, 'south': False, 'east': False, 'west': True}
```

A wall value of `True` means that side of the cell is closed (blocked); `False`
means it's open (passable).

## Accessing the solution

Call `.solve()` to get the shortest path between `entry` and `exit` as a
string of direction letters (`N`, `E`, `S`, `W`):

```python
path = maze.solve()
print(path)   # e.g. "EESSWS"
```

## Notes

- `generate()` must be called before `solve()` or before reading `maze.grid`
  — the grid is empty until generation runs.
- Calling `generate()` again (optionally after changing `maze.seed`) will
  regenerate the maze from scratch.