from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from driver.singletone import Singletone
from util.logger import Logger
from util.config_manager import ConfigManager


class BaseForm:
    """
    Base class for Pages'/ Form's classes
    """
    def __init__(self):
        self.log = Logger
        self.timeout = ConfigManager.get_value_from_config("wait_timeout")

    def is_page_open(self):
        """Check whether page is opened.

        Returns:
            True for success, False otherwise.
        """
        found_marker = False
        try:
            browser = Singletone.get_instance().driver
            self.log.info(f"Check if we on {self.__class__.__name__}")            
            browser.find_element(*self.loc_page_marker)
            found_marker = True            
        except NoSuchElementException as e:
            self.log.error(f"Can't open {self.__class__.__name__} {e}")
        finally:
            return found_marker
            