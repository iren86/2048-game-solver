# -*- coding: utf-8 -*-

import os.path

from selenium import webdriver


class BrowserFactory(object):
    """Factory to build preconfigured browser instance"""

    @staticmethod
    def create_firefox_debug():
        """
        Build firefox instance with debug addons on board.
        """

        firebug_file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../../../../plugins/firefox/firebug.xpi")
        firepath_file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../../../../plugins/firefox/firepath.xpi")

        assert os.path.isfile(firebug_file_path), "Firebug plugin doesn't exist: " + firebug_file_path
        assert os.path.isfile(firepath_file_path), "Firepath plugin doesn't exist: " + firepath_file_path

        fp = webdriver.FirefoxProfile()
        fp.add_extension(extension=firebug_file_path)
        fp.add_extension(extension=firepath_file_path)
        driver = webdriver.Firefox(firefox_profile=fp)
        driver.maximize_window()
        return driver

    @staticmethod
    def create_firefox():
        """
        Build clean firefox instance.
        """

        driver = webdriver.Firefox()
        driver.maximize_window()
        return driver
