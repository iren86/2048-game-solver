# -*- coding: utf-8 -*-

class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""

    PAGE_REQUEST_TIMEOUT_IN_SEC = 2

    def __init__(self, driver):
        self.driver = driver
