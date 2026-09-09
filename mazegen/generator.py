import random
from collections import deque

OPPOSITE = {
    "north": "south",
    "east": "west",
    "south": "north",
    "west": "east",
}

DIRECTION_LETTERS = {
    "north": "N",
    "east": "E",
    "south": "S",
    "west": "W",
}


class Cell:
    """Represents a single cell in the maze grid.

    Attributes:
        x (int): The x-coordinate (horizontal position).
        y (int): The y-coordinate (vertical position).
        visited (bool): Flag indicating whether this cell has been visited.
        walls (dict[str, bool]): Wall status for each of the four
            directions, mapping direction name to whether a wall exists.
    """
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.visited: bool = False
        self.walls: dict[str, bool] = {
            "north": True,
            "south": True,
            "east": True,
            "west": True,
        }


class MazeGenerator:
    """Generates a maze on a grid using recursive backtracking.

    Attributes:
        width (int): Width of the maze.
        height (int): Height of the maze.
        grid (list[list[Cell]]): The maze grid. Empty until generate()
            is called.
        entry (tuple[int, int]): Starting coordinates (x, y) of the maze.
        exit (tuple[int, int]): Ending coordinates (x, y) of the maze.
        perfect (bool): Whether the maze should be a perfect maze
            (exactly one path between any two cells, no loops).
        seed (int | None): Random seed. If None, a random value between
            0 and 100 is generated.
    """
    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        perfect: bool = False,
        seed: int | None = None
    ):
        self.width = width
        self.height = height
        self.grid: list[list[Cell]] = []
        self.entry: tuple[int, int] = entry
        self.exit: tuple[int, int] = exit
        self.perfect = perfect
        if seed is None:
            self.seed = random.randint(0, 100)
        else:
            self.seed = seed

    def build_grid(self) -> list[list[Cell]]:
        """Build a new grid of unvisited, fully-walled cells.

        Returns:
            list[list[Cell]]: A grid of size height x width, where each
                Cell is unvisited and has all four walls closed.
        """
        grid = []
        for h in range(self.height):
            row = []
            for w in range(self.width):
                current_cell = Cell(w, h)
                row.append(current_cell)
            grid.append(row)
        return grid

    def get_valid_neighbors(
        self, current_cell: Cell
    ) -> list[tuple[Cell, str]]:
        """Get the neighboring cells that lie within the grid bounds.

        Args:
            current_cell (Cell): The current cell.

        Returns:
            list[tuple[Cell, str]]: A list of (neighbor cell, direction
                name) pairs for each of the four cardinal directions that
                falls within the grid bounds.
        """
        valid_neighbors: list[tuple[Cell, str]] = []
        north_cell = (current_cell.y - 1, current_cell.x)
        east_cell = (current_cell.y, current_cell.x + 1)
        south_cell = (current_cell.y + 1, current_cell.x)
        west_cell = (current_cell.y, current_cell.x - 1)
        list_direction: list[tuple[tuple[int, int], str]] = [
            (north_cell, "north"),
            (east_cell, "east"),
            (south_cell, "south"),
            (west_cell, "west"),
        ]
        for coordinate, direction in list_direction:
            y, x = coordinate
            if (
                x >= 0 and y >= 0 and x < self.width and y < self.height
            ):  # limit_check
                direction_cell = self.grid[y][x]
                valid_neighbors.append((direction_cell, direction))
        return valid_neighbors

    def get_unvisited_neighbors(
        self, current_cell: Cell
    ) -> list[tuple[Cell, str]]:
        """Get unvisited neighbors from get_valid_neighbors's result.

        Args:
            current_cell (Cell): The current cell.

        Returns:
            list[tuple[Cell, str]]: A list of (neighbor cell, direction
                name) pairs for neighbors that are within grid bounds
                and unvisited.
        """
        valid_neighbors: list[tuple[Cell, str]] = self.get_valid_neighbors(
            current_cell
        )
        unvisited_neighbors: list[tuple[Cell, str]] = []
        for cell, direction in valid_neighbors:
            if cell.visited is False:
                unvisited_neighbors.append((cell, direction))
        return unvisited_neighbors

    def get_connected_neighbors(
        self, current_cell: Cell, visited_bfs: set[tuple[int, int]]
    ) -> list[tuple[Cell, str]]:
        """Get neighbors reachable through an open wall, not yet visited
        by BFS.

        After getting neighbors within grid bounds via get_valid_neighbors,
        collects only those that satisfy both conditions:
            - (cell.x, cell.y) is not yet in visited_bfs (the set of
              coordinates already explored by the caller's BFS)
            - current_cell.walls[direction] is False (i.e. the wall in
              that direction is open, so the cell is actually reachable)

        Args:
            current_cell (Cell): The current cell.
            visited_bfs (set[tuple[int, int]]): Set of coordinates already
                visited by the BFS traversal.

        Returns:
            list[tuple[Cell, str]]: A list of (neighbor cell, direction
                name) pairs for neighbors reachable through an open wall
                and not yet visited.
        """
        valid_neighbors: list[tuple[Cell, str]] = self.get_valid_neighbors(
            current_cell
        )
        connected_neighbors: list[tuple[Cell, str]] = []
        for cell, direction in valid_neighbors:
            if (cell.x, cell.y) not in visited_bfs and current_cell.walls[
                direction
            ] is False:
                connected_neighbors.append((cell, direction))
        return connected_neighbors

    def calc_42patern(self) -> list[tuple[int, int]]:
        """Calculate the coordinates of cells forming the "42" pattern
        at the center of the maze.

        Raises:
            ValueError: If the maze is too small to fit the "42" pattern.

        Returns:
            list[tuple[int, int]]: A list of (y, x) coordinates for the
                cells that make up the "42" pattern.
        """
        patern_height = 5
        patern_width = 7
        patern_42 = ["1000111", "1000001", "1110111", "0010100", "0010111"]
        center_y, center_x = (
            self.height // 2,
            self.width // 2,
        )  # //にすれば、整数だけになる（小数切り捨て)
        close_cells: list[tuple[int, int]] = []
        if self.width >= patern_width + 2 and self.height >= patern_height + 2:
            start_y = center_y - (patern_height // 2)
            start_x = center_x - (patern_width // 2)
            for y_index, row in enumerate(patern_42):
                for x_index, bit in enumerate(row):
                    if bit == "1":
                        close_cells.append(
                            (start_y + y_index, start_x + x_index)
                        )
        else:
            raise ValueError(
                f"42 pattern requires width >= {patern_width + 2},"
                f" and height >= {patern_height + 2}."
                f"Current: width={self.width}, height={self.height}",
            )
        return close_cells

    def close_cells(self, cells_list: list[tuple[int, int]]) -> None:
        """Close all walls of the given cells and mark them visited.

        Used to exclude the "42" pattern cells (computed by
        calc_42patern) from the maze generation traversal. Closes both
        the target cell's own walls and the corresponding walls on its
        neighbors.

        Args:
            cells_list (list[tuple[int, int]]): List of (y, x)
                coordinates for the cells to close.
        """
        for cell_y, cell_x in cells_list:
            cell = self.grid[cell_y][cell_x]
            for direction in cell.walls:
                cell.walls[direction] = True
            for neighbor, direction in self.get_valid_neighbors(cell):
                neighbor.walls[OPPOSITE[direction]] = True
            cell.visited = True

    def get_dead_ends(self) -> list[Cell]:
        """Get the list of dead-end cells.

        Scans every cell in the grid and counts how many of its walls
        are closed (True). A cell with exactly 3 closed walls (i.e. only
        one open direction) is considered a dead end.
        Cells with all 4 walls closed (e.g. the "42" pattern) are excluded.

        Returns:
            list[Cell]: The list of dead-end cells.
        """
        dead_ends = []
        for h in range(self.height):
            for w in range(self.width):
                current_cell = self.grid[h][w]
                walls_count = sum(
                    1 for val in current_cell.walls.values() if val is True
                )
                if walls_count == 3:
                    dead_ends.append(current_cell)
        return dead_ends

    def braid(self, pattern_cells: list[tuple[int, int]]) -> None:
        """Randomly open one wall per dead-end cell to create loops
        (braiding).

        Scans all current dead-end cells (from get_dead_ends). For each
        one, collects neighboring directions that are currently walled
        off and not part of pattern_cells (protected cells). If any
        candidates exist, randomly picks one direction and opens the
        wall on both sides to connect the cells. If there are no
        candidates, the cell remains a dead end. This reduces dead ends
        and introduces loops (alternate routes).

        Args:
            pattern_cells (list[tuple[int, int]]): List of (y, x)
                coordinates for cells whose walls must not be broken.
                Typically the "42" pattern coordinates.
        """
        dead_ends = self.get_dead_ends()
        for current_cell in dead_ends:
            list_directions: list[tuple[Cell, str]] = []
            valid_neighbors: list[tuple[Cell, str]] = self.get_valid_neighbors(
                current_cell
            )
            for cell, direction in valid_neighbors:
                if current_cell.walls[direction] is True:
                    if (cell.y, cell.x) in pattern_cells:
                        continue
                    list_directions.append((cell, direction))
            if not list_directions:
                continue
            next_cell, chosen_direction = random.choice(list_directions)
            current_cell.walls[chosen_direction] = False
            next_cell.walls[OPPOSITE[chosen_direction]] = False

    def get_reachable_cells(
        self, start_cell: Cell, restrict_to: set[tuple[int, int]] | None = None
    ) -> set[tuple[int, int]]:
        """Find all cell coordinates reachable from a starting cell via
        BFS.

        Args:
            start_cell (Cell): The cell to start the search from.
            restrict_to (set[tuple[int, int]] | None): A set of
                coordinates to limit the search to. If given, the
                traversal will not expand beyond these coordinates.
                If None, the entire maze is searched.

        Returns:
            set[tuple[int, int]]: The set of (x, y) coordinates
                reachable from start_cell.
        """
        # BFSでは近い場所から順に広げて探索していく
        # ➡︎queue[行列]の先入先出し(FIFO)が適している　先頭と末尾以外取り出さない
        queue = deque([start_cell])  # queue[行列]を作成
        visited: set[tuple[int, int]] = {(start_cell.x, start_cell.y)}
        while queue:
            current_cell = queue.popleft()  # 行列の先頭から1つ取り出す
            # get_connected_neighborsは(Cell, 方向名)のタプルを返すが
            # 方向名は使わないので_で捨てている
            for next_cell, _ in self.get_connected_neighbors(
                current_cell, visited
            ):
                coord = (next_cell.x, next_cell.y)  # 隣接セルの座標

                # restrict_toが指定されていない（None）または、
                # 指定されているがその座標がrestrict_to集合に含まれている時
                if restrict_to is None or coord in restrict_to:
                    visited.add(coord)
                    queue.append(next_cell)  # 行列の末尾に新しく追加する
        return visited

    def is_block_fully_connected(self, x: int, y: int) -> bool:
        """Check whether every cell in a 3x3 block is reachable from
        every other cell through open walls.

        Runs a BFS starting from the block's top-left cell, restricted
        to this 3x3 block, and checks whether all 9 cells are reached.

        Args:
            x (int): The x-coordinate of the block's top-left corner.
            y (int): The y-coordinate of the block's top-left corner.

        Returns:
            bool: True if all 9 cells in the block are reachable,
                False if only some of them are.
        """
        block_cells: set[tuple[int, int]] = set()
        for row in range(y, y + 3):
            for col in range(x, x + 3):
                block_cells.add((col, row))
        start_cell = self.grid[y][x]

        # 左上のセルから、この3x3のブロック内だけでBFSして、到達可能な座標を求める
        visited = self.get_reachable_cells(start_cell, restrict_to=block_cells)
        return len(block_cells) == len(visited)

    def check_maze_connected(self) -> bool:
        """Check whether every cell in the maze is reachable from entry.

        Uses get_reachable_cells starting from the entry cell, and
        compares the number of reachable coordinates to the total
        number of cells (width x height) in the maze.

        Returns:
            bool: True if all cells are reachable from entry,
                False if at least one cell is unreachable.
        """
        entry_x, entry_y = self.entry
        start_cell = self.grid[entry_y][entry_x]
        visited = self.get_reachable_cells(start_cell)
        # 到達可能なセルと、迷路全体のセル数(width * height)が等しいか
        return len(visited) == self.width * self.height

    def find_extra_connections(
            self, row: int, col: int
    ) -> list[tuple[Cell, Cell, str]]:
        """Find all open (unwalled) connections within a 3x3 block.

        For each of the 9 cells in the block, collects neighbors that
        are reachable through an open wall and that also lie within
        the same block. Connections leading outside the block are
        excluded.

        Args:
            row (int): The y-coordinate of the block's top-left corner.
            col (int): The x-coordinate of the block's top-left corner.

        Returns:
            list[tuple[Cell, Cell, str]]: A list of (current cell,
                neighbor cell, direction) tuples representing
                candidate connections that could be closed off.
        """
        block_cells: set[tuple[int, int]] = set()
        candidates: list[tuple[Cell, Cell, str]] = []
        for r in range(row, row + 3):
            for c in range(col, col + 3):
                block_cells.add((c, r))

        for r in range(row, row + 3):
            for c in range(col, col + 3):
                current_cell = self.grid[r][c]
                valid_neighbors = self.get_valid_neighbors(current_cell)
                for cell, direction in valid_neighbors:
                    is_open = current_cell.walls[direction] is False
                    is_in_block = (cell.x, cell.y) in block_cells
                    if is_open and is_in_block:
                        candidates.append((current_cell, cell, direction))
        return candidates

    def remove_extra_connections(
        self, row: int, col: int, candidates: list[tuple[Cell, Cell, str]]
    ) -> None:
        """Close walls to break up an over-connected 3x3 block.

        Randomly picks a connection from candidates, closes the wall on
        both sides, and checks the result. If closing it breaks overall
        maze connectivity, the wall is reopened and the next candidate
        is tried. The loop stops as soon as the block is no longer fully
        connected. If no candidate works, the method simply ends.

        Args:
            row (int): The y-coordinate of the block's top-left corner.
            col (int): The x-coordinate of the block's top-left corner.
            candidates (list[tuple[Cell, Cell, str]]): Candidate
                connections as (current cell, neighbor cell, direction)
                tuples, as returned by find_extra_connections.
        """
        while candidates:
            cell_to_close, neighbor_cell, direction_to_close = random.choice(
                candidates
            )
            # 壁閉じる
            cell_to_close.walls[direction_to_close] = True
            neighbor_cell.walls[OPPOSITE[direction_to_close]] = True

            candidates.remove(
                (cell_to_close, neighbor_cell, direction_to_close)
            )  # 選ばれたものを候補から削除し、もう選ばれないようにする

            # 壁を閉じてみたが、その結果行けないセルが出来た
            # 壁を閉じて元に戻し、次の候補へ
            if not self.check_maze_connected():
                cell_to_close.walls[direction_to_close] = False
                neighbor_cell.walls[OPPOSITE[direction_to_close]] = False
                continue

            # 壁を閉じた結果、3x3ブロックがもう全部つながっている状態ではなくなった
            # 目的達成なのでループを抜ける
            if not self.is_block_fully_connected(col, row):
                break

    def fix_large_open_areas(
        self,
    ) -> None:
        """Scan every 3x3 block in the grid and fix over-open areas by
        adding walls.

        Checks each 3x3 block, using its top-left coordinates (row, col)
        over the range height - 2, width - 2. If a block is fully
        connected (i.e. an over-open area with too few walls), collects
        candidate connections via find_extra_connections and closes
        some of them via remove_extra_connections.
        """
        for row in range(self.height - 2):  # 3x3ブロックの左上として使えるrowの上限
            for col in range(self.width - 2):
                # その3x3ブロックが「全部繋がっている」＝壁が無さすぎる（3x3の開けた空間ができている）かをチェック
                if self.is_block_fully_connected(col, row):
                    candidates = self.find_extra_connections(row, col)
                    self.remove_extra_connections(row, col, candidates)

    def generate(self) -> None:
        """Generate the maze using the recursive backtracker algorithm.

        Steps:
            1. Build the grid and close the "42" pattern cells (raises
               an error if entry or exit overlaps the pattern).
            2. Carve the maze from entry via DFS (depth-first search),
               breaking walls into unvisited neighbors and backtracking
               at dead ends.
            3. Fix over-open 3x3 areas via fix_large_open_areas. If
               perfect is False, additionally alternates braid and
               fix_large_open_areas twice to reduce dead ends (not
               guaranteed to eliminate them entirely).

        Raises:
            ValueError: If the entry or exit coordinates overlap the
                "42" pattern.
        """
        self.grid = self.build_grid()  # gridを新規作成
        close_cell_list = self.calc_42patern()  # 42patern座標を計算

        # self.entry/self.exit は (x, y) 順だが、close_cell_list は (y, x) 順
        # （self.grid[y][x] でアクセスするため）なので、↓のifで比較する前に順序を揃える
        entry_yx = (self.entry[1], self.entry[0])
        exit_yx = (self.exit[1], self.exit[0])

        # entry/exitが42パターンと重なっていないかチェック
        if (entry_yx in close_cell_list) or (exit_yx in close_cell_list):
            raise ValueError(
                f"Entry {self.entry} or exit {self.exit} "
                "overlaps with the '42' pattern; "
                "choose different entry/exit coordinates "
                "or a larger maze size."
            )  # 重なっていたらValueError
        else:  # 問題なければセルを閉じる
            self.close_cells(close_cell_list)

        random.seed(self.seed)  # seedを固定
        stack: list[Cell] = []
        # entryセルをスタックに入れ訪問済みに
        start_cell = self.grid[self.entry[1]][self.entry[0]]
        start_cell.visited = True
        stack.append(start_cell)

        while stack:
            current_cell = stack[-1]  # スタックの末尾（現在地）を見る　= stack[len(stack)-1]
            neighbors = self.get_unvisited_neighbors(current_cell)
            # 未訪問の隣接セルがあれば、ランダムに1つ選んで壁を壊して繋げ、スタックに積んでいく
            if neighbors:
                next_cell, direction = random.choice(neighbors)
                current_cell.walls[direction] = False
                # 壁を壊す（２つのセル(current_cell , next_cell)の壁情報を変えないといけない
                # どの方向を壊すか→direction　next_cellは反対の方向になるのでOPPOSITE[direction]
                next_cell.walls[OPPOSITE[direction]] = False
                next_cell.visited = True
                stack.append(next_cell)
            else:  # 未訪問の隣が無ければ、スタックから降ろす
                stack.pop()

        self.fix_large_open_areas()
        if self.perfect is False:
            for _ in range(2):  # 2回も繰り返せば、大抵の行き止まりは十分減るので2にした
                self.braid(close_cell_list)  # 行き止まり解消→壁を壊すので3x3ができるかも
                self.fix_large_open_areas()  # 出来てしまった3x3を潰す

    def solve(self) -> str:
        """Find the shortest path from entry to exit via BFS and
        return it as a direction string.

        Runs a breadth-first search from entry, recording in
        came_from_dic which cell and direction each cell was reached
        from.
        Once exit is reached, the search stops, and the path is
        reconstructed by walking came_from_dic backwards from exit to
        entry, collecting the direction taken at each step.
        The resulting list is reversed to restore entry-to-exit order.

        Returns:
            str: The shortest path from entry to exit, as a
                concatenation of N/E/S/W direction characters.
        """
        start_cell = self.grid[self.entry[1]][self.entry[0]]
        # BFS用のキューを作成、開始セルを入れる (DFSのstackの役割)
        queue: deque[Cell] = deque()
        queue.append(start_cell)
        # BFS探索済み座標の集合を用意し、開始セルを訪問済みにする
        visited_bfs: set[tuple[int, int]] = set()
        visited_bfs.add((start_cell.x, start_cell.y))

        # 「どのセルから、どの方向に進んでこのセルに来たか」を記録する辞書。
        # キーは到達したセルの座標、値は「(元セル, 進んだ方向)」 → 戻る時に必要
        came_from_dic: dict[tuple[int, int], tuple[Cell, str]] = {}

        while queue:
            current_cell = queue.popleft()
            if (
                current_cell.x == self.exit[0]
                and current_cell.y == self.exit[1]
            ):  # 取り出したセルがexitと一致したら、探索を終了
                break
            else:  # exitでなければ、壁が無くBFS未探索の隣接セルを取得
                connected_neighbors = self.get_connected_neighbors(
                    current_cell, visited_bfs
                )

                # それぞれについて、訪問済みに追加し、
                # 「どこから来たか」をcame_from_dicに記録し、queueに追加
                for next_cell, direction in connected_neighbors:
                    visited_bfs.add((next_cell.x, next_cell.y))
                    came_from_dic[(next_cell.x, next_cell.y)] = (
                        current_cell,
                        direction,
                    )
                    queue.append(next_cell)

        #  exitからcame_from_dicを逆にたどってentryまで戻る
        path: list[str] = []
        current = (self.exit[0], self.exit[1])
        entry_cell = (self.entry[0], self.entry[1])
        # currentがexitの状態でループへ
        while current != entry_cell:
            prev_cell, direction = came_from_dic[current]  # 1つ前のセルと進んだ方向を取得
            letter = DIRECTION_LETTERS[direction]  # その方向の文字（N/E/S/W）をpathに追加
            path.append(letter)                     # pathに追加
            current = (prev_cell.x, prev_cell.y)  # currentを1つ前のセルに更新
        path.reverse()  # entryまで戻ったら、それまでのpathを逆順に
        return "".join(path)  # 文字リストを1つの文字列に連結して返す（例："ESEE..."）
