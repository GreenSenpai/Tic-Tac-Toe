import os
from abc import ABC, abstractmethod

# ——— Abstraction ———
class Game(ABC):
    @abstractmethod
    def make_move(self, row: int, col: int) -> bool:
        """Attempt to play at (row, col). Return True if successful."""
        pass

    @abstractmethod
    def check_winner(self) -> str | None:
        """Return 'X', 'O', 'Tie', or None if the game is still ongoing."""
        pass

    @abstractmethod
    def display(self) -> None:
        """Show the current board."""
        pass

    @abstractmethod
    def run(self) -> None:
        """Drive the main game loop."""
        pass

class Saver(ABC):
    @abstractmethod
    def save(self, text: str) -> None:
        """Persist a line of text."""
        pass

    @abstractmethod
    def load(self) -> str:
        """Load all saved lines as one big string."""
        pass


# ——— Inheritance + Encapsulation + Aggregation ———
class TicTacToeGame(Game):
    def __init__(self, saver: Saver):
        self._board = [[" "]*3 for _ in range(3)]
        self._current = "X"
        self._moves = 0
        self._saver = saver

    def make_move(self, row, col):
        # row and col are 0-based internally
        if not (0 <= row < 3 and 0 <= col < 3):
            return False
        if self._board[row][col] != " ":
            return False
        self._board[row][col] = self._current
        self._moves += 1
        return True

    def check_winner(self):
        b = self._board
        lines = (
            [b[i][0] + b[i][1] + b[i][2] for i in range(3)] +    # rows
            [b[0][i] + b[1][i] + b[2][i] for i in range(3)] +    # cols
            [b[0][0] + b[1][1] + b[2][2], b[0][2] + b[1][1] + b[2][0]]  # diags
        )
        for line in lines:
            if line == "XXX":
                return "X"
            if line == "OOO":
                return "O"
        if self._moves == 9:
            return "Tie"
        return None

    def display(self):
        print("\n".join(" | ".join(self._board[r]) for r in range(3)))
        print()

    def run(self):
        print("Starting Tic‑Tac‑Toe!")
        while True:
            self.display()
            move = input(f"Player {self._current}, enter row,col (1–3): ")
            try:
                r_input, c_input = map(int, move.split(","))
            except ValueError:
                print("Invalid format. Use two numbers 1–3 separated by a comma.")
                continue

            # convert to 0-based
            r, c = r_input - 1, c_input - 1

            if not self.make_move(r, c):
                print("Move invalid or cell taken, try again (rows/cols 1–3).")
                continue

            winner = self.check_winner()
            if winner:
                self.display()
                msg = "It's a Tie!" if winner == "Tie" else f"Player {winner} wins!"
                print(msg)
                self._saver.save(msg)
                break

            # switch player
            self._current = "O" if self._current == "X" else "X"

    def reset(self):
        """Clear the board and move counter, keep same saver."""
        self._board = [[" "]*3 for _ in range(3)]
        self._current = "X"
        self._moves = 0


# ——— Polymorphism ———
class FileSaver(Saver):
    def __init__(self, filename="results.txt"):
        self.filename = filename

    def save(self, text: str):
        with open(self.filename, "a") as f:
            f.write(text + "\n")

    def load(self) -> str:
        if not os.path.exists(self.filename):
            return "(no results yet)\n"
        with open(self.filename) as f:
            return f.read()

class ConsoleSaver(Saver):
    def save(self, text: str):
        print(f"(would save) → {text}")

    def load(self) -> str:
        return "(console‑only, no file)\n"


# ——— Decorator ———
class LoggedGame(Game):
    def __init__(self, game: Game):
        self._game = game

    def make_move(self, row: int, col: int) -> bool:
        # Logging uses 1-based coordinates for clarity
        print(f"[LOG] Player {self._game._current} → move at ({row+1}, {col+1})")
        return self._game.make_move(row, col)

    def check_winner(self) -> str | None:
        return self._game.check_winner()

    def display(self) -> None:
        self._game.display()

    def run(self) -> None:
        self._game.run()


# ——— Main CLI with Restart Option ———
def main():
    print("1) Play a new game")
    print("2) View past results")
    choice = input("Select 1 or 2: ").strip()

    saver: Saver = FileSaver("results.txt")

    if choice == "2":
        print("\n=== Past Results ===")
        print(saver.load())
        return

    base_game = TicTacToeGame(saver)
    game = LoggedGame(base_game)

    while True:
        base_game.reset()
        game.run()
        again = input("Play again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
