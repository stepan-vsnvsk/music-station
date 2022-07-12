from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from driver.singletone import Singletone
from util.config_manager import ConfigManager
from util.logger import Logger


class DriverUtil:
    """Wrapper around Webdriver functionality to work with windows, tabs."""
    def __init__(self):
        self.driver = Singletone.get_instance().driver
        self.log = Logger
        self.timeout = ConfigManager.get_value_from_config("wait_timeout")
        self.image_path = ConfigManager.get_value_from_config("image_path")
        self.image_ext = ConfigManager.get_value_from_config("image_extension")

    def navigate_to(self, url):
        """Open URL.

        Args:
            url(str): URL
        """
        self.log.info(f"Navigate to {url}") 
        self.driver.get(url)

    def screenshot(self, name):
        """Save a screenshot.

        Args:
            name(str): name of a file to save.
        """        
        filename = self.image_path + name + self.image_ext
        self.log.info(f"Save screenshot {filename}")        
        self.driver.save_screenshot(filename)

    def original_window_id(self):
        """Get current window id.

        Returns:
            window's ID (str)
        """
        self.log.info("Save current window id") 
        return self.driver.current_window_handle

    def switch_to_new_window(self, original_window):
        """Switch to a new window.

        Iterate over open windows and go not to a current one.
        """
        WebDriverWait(self.driver, self.timeout).until(
            EC.number_of_windows_to_be(2))      
        self.log.info("Switch to New Tab")
        for window_handle in self.driver.window_handles:
            if window_handle != original_window:
                self.driver.switch_to.window(window_handle)
                break

    def close_tab(self):
        """Close current tab."""
        self.log.info("Close current tab")
        self.driver.close()

    def switch_to_original_window(self, window_id):
        """Switch to window with that ID.

        Args:
            window_id(str): previously saved window's ID
        """
        self.log.info(f"Switch to original window {window_id}")
        self.driver.switch_to.window(window_id)

    def switch_to_default_content(self):
        """Switch back from iframe"""
        self.log.info("Switch back to 'default content' from iframe")
        self.driver.switch_to.default_content()
