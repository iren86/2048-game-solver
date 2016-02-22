# -*- coding: utf-8 -*-

from random import randint

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from BasePage import BasePage


class GameEvent(object):
    """Game page action event."""
    NOT_INITIALIZED = -1
    END_GAME_EVENT = 0
    STEP_LEFT_EVENT = 1
    STEP_RIGHT_EVENT = 2
    STEP_UP_EVENT = 3
    STEP_DOWN_EVENT = 4

    def __init__(self, event_type=NOT_INITIALIZED, game_board=None, score=0):
        if game_board is None:
            game_board = []
        self.event_type = event_type
        self.game_board = game_board
        self.score = score

    def get_event_type_string(self):
        """Return string representation of game event type"""
        if self.event_type == GameEvent.NOT_INITIALIZED:
            return "≈ Not Initialized".decode('utf-8')
        elif self.event_type == GameEvent.STEP_LEFT_EVENT:
            return "← Event".decode('utf-8')
        elif self.event_type == GameEvent.STEP_RIGHT_EVENT:
            return "→ Event".decode('utf-8')
        elif self.event_type == GameEvent.STEP_UP_EVENT:
            return "↑ Event".decode('utf-8')
        elif self.event_type == GameEvent.STEP_DOWN_EVENT:
            return "↓ Event".decode('utf-8')
        elif self.event_type == GameEvent.END_GAME_EVENT:
            return "☺ End Game Event".decode('utf-8')

        raise ValueError("Event type not supported.")

    def is_step_event(self):
        return self.event_type in (
            GameEvent.STEP_LEFT_EVENT, GameEvent.STEP_RIGHT_EVENT,
            GameEvent.STEP_UP_EVENT, GameEvent.STEP_DOWN_EVENT)

    def is_game_event(self):
        return self.event_type == GameEvent.END_GAME_EVENT


class GamePage(BasePage):
    """Game page action methods come here."""
    SCORE_CONTAINER = (By.CLASS_NAME, 'score-container')
    NEW_GAME_BUTTON = (By.CLASS_NAME, 'restart-button')
    GAME_BOARD_GRID_CONTAINER = (By.CLASS_NAME, 'grid-container')
    GAME_WON_MESSAGE_CONTAINER = (By.CSS_SELECTOR, 'div.game-message.game-won')
    GAME_OVER_MESSAGE_CONTAINER = (By.CSS_SELECTOR, 'div.game-message.game-over')
    GAME_BOARD_GRID_ROWS = (By.CLASS_NAME, 'grid-row')
    GAME_BOARD_GRID_CELLS = (By.CLASS_NAME, 'grid-cell')
    GAME_BOARD_GRID_TILES = (By.CLASS_NAME, 'tile')

    def __init__(self, driver):
        BasePage.__init__(self, driver)
        self.handlers = set()

    def is_game_over(self):
        """Verifies that game over message appears on the page"""
        try:
            self.driver.find_element(*GamePage.GAME_OVER_MESSAGE_CONTAINER)
            return True
        except NoSuchElementException as e:
            return False

    def is_game_won(self):
        """Verifies that game won message appears on the page"""
        try:
            self.driver.find_element(*GamePage.GAME_WON_MESSAGE_CONTAINER)
            return True
        except NoSuchElementException as e:
            return False

    def is_title_matches(self):
        """Verifies that the hardcoded text "2048" appears in page title"""
        return "2048" in self.driver.title

    def push_left(self):
        """Use left arrow key to move the tiles left"""
        self.driver.find_element(*GamePage.GAME_BOARD_GRID_CONTAINER).send_keys(Keys.ARROW_LEFT)

    def push_right(self):
        """Use right arrow key to move the tiles right"""
        self.driver.find_element(*GamePage.GAME_BOARD_GRID_CONTAINER).send_keys(Keys.ARROW_RIGHT)

    def push_up(self):
        """Use up arrow key to move the tiles up"""
        self.driver.find_element(*GamePage.GAME_BOARD_GRID_CONTAINER).send_keys(Keys.ARROW_UP)

    def push_down(self):
        """Use down arrow key to move the tiles down"""
        self.driver.find_element(*GamePage.GAME_BOARD_GRID_CONTAINER).send_keys(Keys.ARROW_DOWN)

    def new_game(self):
        """Create a new game"""
        element = self.driver.find_element(*GamePage.NEW_GAME_BUTTON)
        element.click()

    def bot_play(self):
        """Start a game"""
        while not self.is_game_over() \
                and not self.is_game_won():
            event_type = GameEvent.NOT_INITIALIZED
            num = randint(0, 3)
            if num == 0:
                self.push_left()
                event_type = GameEvent.STEP_LEFT_EVENT
            elif num == 1:
                self.push_right()
                event_type = GameEvent.STEP_RIGHT_EVENT
            elif num == 2:
                self.push_up()
                event_type = GameEvent.STEP_UP_EVENT
            else:
                self.push_down()
                event_type = GameEvent.STEP_DOWN_EVENT
            self.notify_handlers(self.build_event(event_type))
        self.notify_handlers(self.build_event(GameEvent.END_GAME_EVENT))

    def build_event(self, event_type):
        """Build game event"""
        result = []
        grid_rows = WebDriverWait(self.driver, BasePage.PAGE_REQUEST_TIMEOUT_IN_SEC).until(
            EC.presence_of_all_elements_located(GamePage.GAME_BOARD_GRID_ROWS)
        )
        for grid_row in grid_rows:
            grid_cells = grid_row.find_elements(*GamePage.GAME_BOARD_GRID_CELLS)
            result.append([0] * len(grid_cells))

        self.update_cells(result)
        score = self.get_score()
        return GameEvent(event_type, result, score)

    def notify_handlers(self, event):
        """Notify all registered handlers"""
        for handler in self.handlers:
            handler(event)

    def add_game_handler(self, handler):
        """Register a handler"""
        self.handlers.add(handler)

    def remove_game_handler(self, handler):
        """Unregister a handler"""
        self.handlers.remove(handler)

    def get_score(self):
        """Return current game score"""
        element = self.driver.find_element(*GamePage.SCORE_CONTAINER)
        text = element.text

        if element.text == "":
            return 0

        return text.strip().splitlines()[0]

    def update_cells(self, result):
        """Update board cells. Input result list must be filled with zeros."""
        grid_tiles = WebDriverWait(self.driver, BasePage.PAGE_REQUEST_TIMEOUT_IN_SEC).until(
            EC.presence_of_all_elements_located(GamePage.GAME_BOARD_GRID_TILES)
        )
        for grid_tile in grid_tiles:
            tile_cls = grid_tile.get_attribute("class")
            # [tile tile-2 tile-position-4-3 tile-new]
            tile_cls_lst = tile_cls.strip().split(" ")
            if "tile-merged" in tile_cls_lst:
                continue

            # tile-2
            tile_num = int(tile_cls_lst[1].split("-")[1])
            # tile-position-4-3
            # -> [4, 3]
            tile_pos_yx_lst = tile_cls_lst[2].split("-")[-2:]
            # -> 3 -1
            tile_row_idx = int(tile_pos_yx_lst[1]) - 1
            # -> 4 -1
            tile_col_idx = int(tile_pos_yx_lst[0]) - 1
            result[tile_row_idx][tile_col_idx] += tile_num
