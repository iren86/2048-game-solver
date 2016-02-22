# -*- coding: utf-8 -*-

import unittest2

from com.solver.game.common.BrowserFactory import BrowserFactory
from com.solver.game.common.GameLogger import create_logger
from com.solver.game.common.LogDecorator import log_errors
from com.solver.game.page.GamePage import GamePage


class GamePageTest(unittest2.TestCase):
    """A test class to test game page"""

    logger = create_logger()

    def setUp(self):
        self.driver = BrowserFactory.create_firefox_debug()
        self.driver.get("http://gabrielecirulli.github.io/2048/")

    def tearDown(self):
        self.driver.quit()

    def handle_game_step_event(self, game_event):
        GamePageTest.logger.info(
            "%s / %s" % (game_event.get_event_type_string(), game_event.score))
        board_state = ""
        for row_index, row_item in enumerate(game_event.game_board):
            row_str = ""
            for col_index, col_item in enumerate(game_event.game_board[row_index]):
                row_str += "\t|\t" + str(game_event.game_board[row_index][col_index])
            row_str += "\t|"
            board_state += row_str + "\n"

        GamePageTest.logger.info(
            "\n[%s] Board State:\n%s" % (game_event.score, board_state))

    def handle_end_game_event(self, game_event):
        GamePageTest.logger.info(
            "%s. Score: %s" % (game_event.get_event_type_string(), game_event.score))

    def game_event_handler(self, game_event):
        if game_event.is_step_event():
            self.handle_game_step_event(game_event)
        elif game_event.is_game_event():
            self.handle_end_game_event(game_event)

    @log_errors
    def test_game_play(self):
        """
        Tests game play.
        Note that it does not follow any strategy.
        This test perform random actions to play the game.
        """

        # Load the game page
        game_page = GamePage(self.driver)
        game_page.add_game_handler(self.game_event_handler)

        # Checks if we have correct page loaded
        assert game_page.is_title_matches(), "Game page title doesn't match."

        # start new game
        game_page.new_game()
        # start playing
        game_page.bot_play()


if __name__ == "__main__":
    unittest2.main()
