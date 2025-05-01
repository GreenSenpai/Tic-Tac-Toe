import unittest
from unittest.mock import patch, MagicMock
from io import StringIO


from main import TicTacToeGame, Saver, FileSaver, ConsoleSaver, LoggedGame

# Dummy Saver for isolated testing
class DummySaver(Saver):
    def __init__(self):
        self.saved_text = ""
    def save(self, text: str):
        self.saved_text = text
    def load(self) -> str:
        return self.saved_text

class TestTicTacToeGame(unittest.TestCase):
    def setUp(self):
        self.saver = DummySaver()
        self.game = TicTacToeGame(self.saver)

    def test_valid_move(self):
        result = self.game.make_move(0, 0)
        self.assertTrue(result)
        self.assertEqual(self.game._board[0][0], "X")

    def test_invalid_move_out_of_bounds(self):
        self.assertFalse(self.game.make_move(3, 3))  # invalid index

    def test_invalid_move_cell_taken(self):
        self.game.make_move(0, 0)
        self.assertFalse(self.game.make_move(0, 0))  # already taken

    def test_win_row(self):
        self.game._board = [
            ["X", "X", "X"],
            [" ", "O", " "],
            ["O", " ", " "]
        ]
        self.game._moves = 5
        self.assertEqual(self.game.check_winner(), "X")

    def test_tie(self):
        self.game._board = [
            ["X", "O", "X"],
            ["X", "O", "O"],
            ["O", "X", "X"]
        ]
        self.game._moves = 9
        self.assertEqual(self.game.check_winner(), "Tie")

    def test_game_reset(self):
        self.game.make_move(0, 0)
        self.game.reset()
        self.assertEqual(self.game._board, [[" "] * 3 for _ in range(3)])
        self.assertEqual(self.game._current, "X")
        self.assertEqual(self.game._moves, 0)

class TestSaverImplementations(unittest.TestCase):
    def setUp(self):
        self.test_filename = "test_results.txt"
        self.filesaver = FileSaver(self.test_filename)
        self.consolesaver = ConsoleSaver()

    def tearDown(self):
        import os
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_filesaver_save_and_load(self):
        self.filesaver.save("Test result")
        content = self.filesaver.load()
        self.assertIn("Test result", content)

    def test_consolesaver_does_not_save(self):
        with patch("builtins.print") as mock_print:
            self.consolesaver.save("Hello")
            self.assertIn("Hello", mock_print.call_args[0][0])

class TestLoggedGame(unittest.TestCase):
    def setUp(self):
        self.dummy_game = TicTacToeGame(DummySaver())
        self.logged_game = LoggedGame(self.dummy_game)

    def test_logged_make_move(self):
        with patch("builtins.print") as mock_print:
            self.logged_game.make_move(0, 1)
            self.assertTrue(mock_print.called)
            self.assertIn("[LOG]", mock_print.call_args[0][0])
            self.assertEqual(self.dummy_game._board[0][1], "X")

    def test_logged_methods_delegate(self):
        # Make sure other methods don't break
        self.assertIsNone(self.logged_game.check_winner())
        self.logged_game.reset = self.dummy_game.reset  # add reset to LoggedGame for testing
        self.logged_game.reset()
        self.assertEqual(self.dummy_game._board, [[" "] * 3 for _ in range(3)])

