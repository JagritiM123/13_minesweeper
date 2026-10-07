from board import Board, DIFFICULTIES


class Minesweeper:
    def __init__(self):
        self.board = None
        self.difficulty = None

    def choose_difficulty(self):
        print("\nChoose difficulty:")
        print("1. Easy   - 6 x 6   - 6 mines")
        print("2. Medium - 9 x 9   - 12 mines")
        print("3. Hard   - 12 x 12 - 24 mines")

        choices = {
            "1": "easy",
            "2": "medium",
            "3": "hard",
            "easy": "easy",
            "medium": "medium",
            "hard": "hard"
        }

        while True:
            choice = input("Difficulty: ").strip().lower()

            if choice in choices:
                self.difficulty = choices[choice]
                settings = DIFFICULTIES[self.difficulty]

                self.board = Board(
                    rows=settings["rows"],
                    cols=settings["cols"],
                    mines=settings["mines"]
                )

                print(f"\nSelected: {self.difficulty.title()}")
                print(
                    f"Board: {settings['rows']} x "
                    f"{settings['cols']}, "
                    f"Mines: {settings['mines']}"
                )

                return

            print("Invalid difficulty. Choose 1, 2, or 3.")

    def display(self, reveal_mines=False):
        b = self.board

        print("\n    " + " ".join(
            f"{c + 1:2}" for c in range(b.cols)
        ))

        for r in range(b.rows):
            cells = []

            for c in range(b.cols):
                pos = (r, c)

                if reveal_mines and pos in b.mines:
                    ch = "*"

                elif pos in b.flags:
                    ch = "F"

                elif pos not in b.revealed:
                    ch = "#"

                elif pos in b.mines:
                    ch = "*"

                else:
                    count = b.adjacent_mines(r, c)

                    if count == 0:
                        ch = "."
                    else:
                        ch = str(count)

                cells.append(f"{ch:2}")

            print(f"{r + 1:2}  " + " ".join(cells))

    def process_reveal(self, r, c):
        pos = (r, c)

        if pos in self.board.flags:
            print("That cell is flagged. Unflag it before revealing.")
            return False

        if pos in self.board.revealed:
            print("That cell has already been revealed.")
            return False

        hit_mine = self.board.reveal(pos)

        if hit_mine:
            self.display(reveal_mines=True)
            print("BOOM! You hit a mine.")
            return True

        print("Reveal successful.")
        return False

    def process_flag(self, r, c):
        pos = (r, c)

        if pos in self.board.revealed:
            print("You cannot flag a revealed cell.")
            return

        if pos in self.board.flags:
            self.board.toggle_flag(pos)
            print("Flag removed.")
        else:
            self.board.toggle_flag(pos)
            print("Cell flagged.")

    def run(self):
        print("\n======================")
        print("     MINESWEEPER")
        print("======================")

        self.choose_difficulty()

        print("\nCommands:")
        print("  r row col  -> reveal")
        print("  f row col  -> flag/unflag")
        print("  q          -> quit")

        while True:
            self.display()

            raw = input("\n> ").strip().lower()

            if raw == "q":
                print("Game ended.")
                return

            parts = raw.split()

            if len(parts) != 3 or parts[0] not in {"r", "f"}:
                print("Use: r row col, f row col, or q.")
                continue

            try:
                r = int(parts[1]) - 1
                c = int(parts[2]) - 1

            except ValueError:
                print("Coordinates must be numbers.")
                continue

            if not self.board.in_bounds(r, c):
                print("Outside the board.")
                continue

            if parts[0] == "f":
                self.process_flag(r, c)
                continue

            game_over = self.process_reveal(r, c)

            if game_over:
                return

            if self.board.won():
                self.display()
                print("\nCongratulations! You cleared the board!")
                print(f"Difficulty: {self.difficulty.title()}")
                return