from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from driver.singletone import Singletone
from util.config_manager import ConfigManager


class FirefoxBrowser(metaclass=Singletone):
    def __init__(self, config: dict):
        """Firefox Browser initiliazition.

        Get config settings, call webdriver, add settings.

        Args:
             config (dict): settings for webdriver.
        """
        config_options, config_methods = ConfigManager.parse_config_for_driver(config)
        options = webdriver.FirefoxOptions()
        if config_options:            
            [options.add_argument(i) for i in config_options]
        self.driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()), options=options)
