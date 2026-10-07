import random


DIFFICULTIES = {
    "easy": {
        "rows": 6,
        "cols": 6,
        "mines": 6
    },
    "medium": {
        "rows": 9,
        "cols": 9,
        "mines": 12
    },
    "hard": {
        "rows": 12,
        "cols": 12,
        "mines": 24
    }
}


class Board:
    def __init__(self, rows=6, cols=6, mines=6):
        self.rows = rows
        self.cols = cols
        self.mine_total = mines

        if mines >= rows * cols:
            raise ValueError(
                "Number of mines must be less than the number of cells."
            )

        self.mines = self._build_mines()
        self.revealed = set()
        self.flags = set()

    def _build_mines(self):
        cells = [
            (r, c)
            for r in range(self.rows)
            for c in range(self.cols)
        ]

        return set(random.sample(cells, self.mine_total))

    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def neighbors(self, r, c):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):

                if dr == 0 and dc == 0:
                    continue

                nr = r + dr
                nc = c + dc

                # Correct boundary check
                if self.in_bounds(nr, nc):
                    yield nr, nc

    def adjacent_mines(self, r, c):
        return sum(
            pos in self.mines
            for pos in self.neighbors(r, c)
        )

    def reveal(self, start):
        if not self.in_bounds(*start):
            return False

        # Don't reveal flagged cells
        if start in self.flags:
            return False

        # Don't reveal an already revealed cell
        if start in self.revealed:
            return False

        stack = [start]
        hit_mine = False

        while stack:
            pos = stack.pop()

            if not self.in_bounds(*pos):
                continue

            if pos in self.revealed or pos in self.flags:
                continue

            self.revealed.add(pos)

            if pos in self.mines:
                hit_mine = True
                continue

            # Flood-fill zero-adjacent cells
            if self.adjacent_mines(*pos) == 0:
                for neighbor in self.neighbors(*pos):
                    if (
                        neighbor not in self.revealed
                        and neighbor not in self.flags
                    ):
                        stack.append(neighbor)

        return hit_mine

    def toggle_flag(self, pos):
        if not self.in_bounds(*pos):
            return False

        if pos in self.revealed:
            return False

        if pos in self.flags:
            self.flags.remove(pos)
        else:
            self.flags.add(pos)

        return True

    def won(self):
        safe_cells = self.rows * self.cols - self.mine_total

        return len(self.revealed) == safe_cells