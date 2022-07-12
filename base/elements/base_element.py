from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from driver.singletone import Singletone
from util.config_manager import ConfigManager
from util.logger import Logger


class BaseElement:
    """
    Base class for all Element's classes
    """
    def __init__(self, loc, name_elem):
        self.locator = loc
        self.name = name_elem
        self.browser = Singletone.get_instance().driver 
        self.timeout = ConfigManager.get_value_from_config("wait_timeout")
        self.log = Logger 

    def find_element(self):
        """Wait of element presence and find webelement.

        Returns:
            WebElement object
        Raises:
          Timeout error: If the condition of wait fails
        """
        self.log.info(f"Find {self.name}")        
        return WebDriverWait(self.browser, timeout=self.timeout).until(
            EC.presence_of_element_located(self.locator))

    def find_elements(self):
        """Wait of elements presence and find webelements.

        Returns:
            WebElement objects (list)
        Raises:
          Timeout error: If the condition of wait fails
        """
        self.log.info(f"Find {self.name} elements")         
        return WebDriverWait(self.browser, timeout=self.timeout).until(
            EC.presence_of_all_elements_located(self.locator))
        
    def is_displayed(self):
        """Check whether a element is displayed on a page.

        Returns:
            True for success, False otherwise.
        """
        self.log.info(f"Check if {self.name} is displayed")
        return self.find_element().is_displayed()

    def click(self):
        """Perform click action on a element."""
        self.log.info(f"Click {self.name}")
        WebDriverWait(self.browser, timeout=self.timeout).until(
            EC.element_to_be_clickable(self.locator)).click()

    def get_text(self):
        """Find element and get text.

        Returns:
            Text (str) from element.
        """
        self.log.info(f"Get text from {self.name}")        
        return self.browser.find_element(*self.locator).text
