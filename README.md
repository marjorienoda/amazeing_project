*This project has been created as part of the 42 curriculum by mnoda-ta, rkato.*

## Description
This project's goal is to build `a_maze_ing.py`, a program that reads
settings from a `config.txt` file and generates a maze embedded with
a "42" pattern (supporting two modes: a perfect maze and a non-perfect maze).

After generation, the maze data is written to the output file specified
by the `OUTPUT_FILE` key, and the maze is displayed on screen in ASCII
format. Users can interactively regenerate the maze, toggle the shortest
path display, and change the wall colors.

## Program flow
When you run `a_maze_ing.py`, processing proceeds in the following
order.

1. **`read_config.py`**: Reads the configuration file (e.g.
   `config.txt`), parses its syntax, and converts each key's value
   into the appropriate type (`int`, `bool`, coordinate tuples, etc.).
2. **`mazegen` (`MazeGenerator`)**: Generates the maze data based on
   the converted configuration.
3. **`make_outputfile.py`**: Writes the generated maze data to the
   file specified by the `OUTPUT_FILE` key.
4. **`display.py`**: Displays the generated maze on screen in ASCII
   format and accepts user operations (regenerating the maze,
   toggling the shortest path display, changing wall colors, etc.).

### Overall function call flow
```
main() [a_maze_ing.py]
├── read_config(config_file)                    # reads the file
│
├── check_required_keys(key_dict)                # checks required keys
│
├── build_maze_config(key_dict)                  # converts values
│   ├── int_convert(WIDTH)
│   ├── int_convert(HEIGHT)
│   ├── coordinate_convert(ENTRY)
│   │   └── int_convert(x, y) x2
│   ├── coordinate_convert(EXIT)
│   │   └── int_convert(x, y) x2
│   ├── bool_convert(PERFECT)
│   └── int_convert(SEED)                        # only if SEED is present
│
├── validate_entry_exit(width, height, entry, exit)
│
├── MazeGenerator(**maze_config)                  # instantiation
│
├── maze.generate()                               # generates the maze
│   ├── build_grid()
│   ├── calc_42pattern()
│   ├── close_cells(pattern_cells)
│   ├── (DFS loop: get_unvisited_neighbors)
│   ├── fix_large_open_areas()                    # runs regardless of perfect
│   │   ├── is_block_fully_open(x, y)
│   │   ├── find_extra_connections(row, col)
│   │   └── remove_extra_connections(row, col, candidates)
│   └── only if perfect=False:
│       ├── (up to 5 times) braid(pattern_cells) → fix_large_open_areas()
│       │   # stops once dead ends are 2 or fewer
│       └── count_independent_loops(pattern_cells)  # final check on loop count
├── build_display_grid(maze)                      # builds the display grid
│   ├── make_grid(maze)
│   ├── add_start_goal(maze, grid)
│   └── fill_42pattern(maze, grid)
│
├── render(base_grid)                             # initial display
│
├── make_output(maze, output_file)                # writes the output file
│   ├── calc_wall_sum(walls_dict)
│   └── convert_hex(num)
│
└── while True:                                    # menu loop
   ├── <1> regenerate: generate → build_display_grid → make_output
   │
   ├── <2> toggle show_path
   │   └── show_solve(maze.solve(), maze, grid)       # only if show_path
   │
   ├── <3> rotate color: red→green→yellow→blue→white(default)
   │   └──change_wall_color(grid, color)             # only if color is set
   │
   ├── render(display_grid)
   └── <4> exit loop
```


## Instructions

- Install dependencies
```bash
    make install
```
This creates a virtual environment named `.venv` and installs the external packages this program depends on (e.g. `typing_extensions`), as listed in `requirements.txt`.

- Run the program
```bash
    make run
```
This runs the program using `config.txt` as the configuration file.  
To use a different configuration file, run it directly instead:
```bash
    python3 a_maze_ing.py <config file>
```

- Remove unneeded files
```bash
    make clean
```
Removes caches generated at runtime (`__pycache__`, `.mypy_cache`) and build artifacts from `make build` (`build`, `dist`, `*.egg-info`).   
Generated maze output files (e.g. `maze.txt`) are not removed.

- Check code style and types
```bash
    make lint
```
or
```bash
    make lint-strict
```
Runs `flake8` and `mypy` (`lint-strict` adds the `--strict` flag).

- Build the pip package
```bash
    make build
```
Builds the reusable `mazegen` module as an installable pip package(`.whl`/`.tar.gz`).


## Resources
We referred to the following resources.
- [Maze generation algorithms](https://www.cs.cmu.edu/~112-s23/notes/student-tp-guides/Mazes.pdf)
- [About random()](https://note.nkmk.me/python-random-choice-sample-choices/)
- [DFS and BFS in maze generation](https://qiita.com/ophhdn/items/fb10c932d44b18d12656)
- [How to use double asterisks](https://note.com/engneer_hino/n/n9c6c6297845d)
- [Defining types with optional keys (NotRequired)](https://zenn.dev/t_yng/articles/bc3d779f4bbb70)
- [About TypedDict](https://qiita.com/fgshun/items/587cbc7b5b06c3676622)
- [Introduction to Google-style Python docstrings](https://qiita.com/11ohina017/items/118b3b42b612e527dc1d)
- [Queue in Python](https://www.geeksforgeeks.org/python/queue-in-python/)
- [deque(): working with queues](https://note.nkmk.me/python-collections-deque/#deque)
- [Overview of Python packaging](https://packaging.python.org/en/latest/overview/)
- [How to package a project](https://packaging.python.org/ja/latest/tutorials/packaging-projects/)
- [About pyproject.toml](https://packaging.python.org/ja/latest/guides/writing-pyproject-toml/)
- [About pyproject.toml (part 2)](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#license)
- [License MIT](https://license.md/licenses/mit-license/)

### How AI was used
Model used: [Claude](claude.ai)
We used AI for the following tasks:
- Organizing the assignment overview
- Generating illustrative diagrams
    Used to organize information while working on `display.py`, and to
    understand `fix_large_open_areas()`.
- Explaining the recursive backtracker algorithm.
- Analyzing errors and proposing improvements
    Example: when mypy flagged an error in `convert_keys` (now
    `build_maze_config`), we had it suggest a design fix.
```bash
    def convert_keys(
            key_dict: dict[str, str],
        ) -> dict[str, int | tuple[int, int] | bool | str] | None:
```
With this approach — looping over one combined dictionary and branching by type to convert each value — mypy couldn't track the types far enough, which caused the error.  
※ A dictionary holds a different type per key, but the type annotation
   only expresses one combined union type, so mypy cannot verify which
   type belongs to which key.
→ So we had it suggest switching to TypedDict, which explicitly
   declares the correct type for each key.
- Code review and edge-case checks
- Fixing, improving, and translating docstrings
- Fixing, improving, and translating README.md


## Config file format

`config.txt` specifies one `KEY=VALUE` pair per line.
Lines starting with `#` are treated as comments and ignored.

| Key | Required | Description | Example |
|---|---|---|---|
| WIDTH | Required | Width of the maze (number of cells) | WIDTH=20 |
| HEIGHT | Required | Height of the maze (number of cells) | HEIGHT=15 |
| ENTRY | Required | Entry coordinates (x,y) | ENTRY=0,0 |
| EXIT | Required | Exit coordinates (x,y) | EXIT=19,14 |
| OUTPUT_FILE | Required | Output filename | OUTPUT_FILE=maze.txt |
| PERFECT | Required | Whether the maze is a perfect maze | PERFECT=True |
| SEED | Optional | If given, this value is used; otherwise a random integer between 0 and 100 is chosen | SEED=42 |


## Algorithm
Algorithm used: recursive backtracker (DFS: depth-first search)

### Explanation of the algorithm
Depth-first search (DFS) is a search method that keeps going as deep as
possible in one direction from the current point, and backtracks to the
previous point once it gets stuck (in contrast to BFS: breadth-first
search, which expands outward from nearby points first).

Applying this to maze generation gives the recursive backtracker
algorithm. Specifically, it repeats the following cycle:

1. From the current cell, randomly pick one neighboring cell that has
   not yet been visited.
2. Break the wall between the current cell and that cell to connect
   them, then move into that cell.
3. If there are no unvisited neighboring cells left (a dead end has
   been reached), backtrack to the previous cell.
4. Repeat steps 1-3 until every cell has been visited.

This process connects the entire maze as a single continuous passage
(a tree structure), producing a "perfect maze" in which exactly one
path exists between any two cells.

### Why we chose this algorithm
We chose this algorithm because the idea of repeatedly breaking a
randomly chosen wall among the eligible candidates was simple and easy
to understand.

### Implementation details (phases of `generate()`)

`generate()` is broadly divided into three phases.

**1: Preparation**
Creates a new grid with `build_grid()`, then closes the "42" pattern
cells computed by `calc_42pattern()` using `close_cells()`. If entry or
exit overlaps the pattern, it's treated as an error.

**2: Carving the maze with DFS**
Starting from the entry cell, it repeatedly picks a random unvisited
neighboring cell, breaks the wall to it, and moves in; when it reaches
a dead end, it backtracks to the previous cell.

**3: Post-processing**
- `fix_large_open_areas()` detects fully-open 3x3 areas (blocks where
 all 12 internal walls are open) and fixes them by adding walls,
 without breaking the maze's overall connectivity. This runs
 regardless of the value of `perfect`.
- If `perfect=False` (Pac-Man mode), it additionally repeats `braid()`
 (which opens one wall per dead end) together with
 `fix_large_open_areas()` until at most two dead ends remain (up to
 5 attempts). It then does a final check that at least two
 independent loops exist, printing a warning if this cannot be
 guaranteed.


## Reusable module

The maze generation logic is implemented as the `MazeGenerator` class
inside the `generator.py` module of the `mazegen` package, and can be
reused independently in other projects.
It is built as an installable pip package named `mazegen-*` (see
`make build`; for detailed usage, also see `mazegen/README.md`).

### Installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Basic usage

```python
from mazegen import MazeGenerator

maze = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(19, 14),
)
maze.generate()

# Access the generated grid structure
print(maze.grid[0][0].walls)

# Get the shortest path from entry to exit
solution = maze.solve()
print(solution)
```

If `perfect` is not specified, it defaults to `False`, generating a
non-perfect (Pac-Man-style) maze that includes loops.

### Custom parameters

```python
maze = MazeGenerator(
    width=30,
    height=20,
    entry=(0, 0),
    exit=(29, 19),
    perfect=True,
    seed=42,
)
```


## Team & project management

### Role assignment

| File | Owner |
|---------|------|
| `mazegen/generator.py` | mnoda-ta (except the `calc_42pattern` function, by rkato) |
| `read_config.py` | rkato |
| `make_outputfile.py` | rkato |
| `display.py` | rkato |
| `a_maze_ing.py` | rkato |
| `Makefile` | mnoda-ta |
| `LICENSE.md` | mnoda-ta |
| `pyproject.toml` | mnoda-ta |
| `README.md` | rkato, mnoda-ta |

We initially split the work by assigning the maze generation algorithm
to mnoda-ta and the display part to rkato.  
After that, whenever a task
was finished, we would review the remaining tasks together and whoever
had free time would pick up the next one.  
Once a task was done, we opened a GitHub Pull Request and merged it
after getting the other person's approval.  
We used a [Google Document](https://docs.google.com/document/d/1fioY9jzPlAP8k5x66gox01MW8rBHqUK5eF2OBc1lST0/edit?usp=sharing)
as a shared notes for task management and progress tracking.

### What went well / What could be improved

**What went well**
- Every time something was implemented, we could get the other
  person's confirmation (each of us could review the other's work).
- Splitting tasks clearly meant there was no duplicated work.
- We were able to communicate without any problems

**What could be improved**
- Since new features became necessary later on and some aspects of usage changed, We think the initial design could have been more solid.
- It would be great if we could implement more additional features. example: maze display animation, use MiniLibX (MLX) library.

### Tools used
- GitHub[https://github.com/marjorienoda/amazeing_project] (code review and merging via Pull Requests)
- Discord (communication)
- Google Document (task management and shared notes)