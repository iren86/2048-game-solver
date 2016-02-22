# -*- coding: utf-8 -*-

import logging
import os

rootLogger = None


def create_logger():
    """Function to build preconfigured logger instance"""

    global rootLogger

    if rootLogger is None:
        rootLogger = logging.getLogger()
        rootLogger.setLevel(logging.INFO)

        log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../../game_2048.log")
        fileHandler = logging.FileHandler(log_file_path, "w")
        fileHandler.setLevel(logging.WARN)
        fileHandler.setFormatter(
            logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"))
        rootLogger.addHandler(fileHandler)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logging.Formatter("%(message)s"))
        rootLogger.addHandler(consoleHandler)

    return rootLogger
