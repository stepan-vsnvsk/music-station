from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from driver.singletone import Singletone
from util.config_manager import ConfigManager


class ChromeBrowser(metaclass=Singletone):
    def __init__(self, config: dict):
        """Chrome Browser initiliazition.

        Get config settings, call webdriver, add settings.

        Args:
             config (dict): settings for webdriver.
        """
        config_options, config_methods = ConfigManager.parse_config_for_driver(config)
        options = webdriver.ChromeOptions()
        if config_options:            
            [options.add_argument(i) for i in config_options]        
        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=options)
