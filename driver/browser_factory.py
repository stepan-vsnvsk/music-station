import os
from driver.chrome_browser import ChromeBrowser
from driver.firefox_browser import FirefoxBrowser
from util.config_manager import ConfigManager


class BrowserFactory:
    BROWSERS = ['chrome', 'firefox']
    
    @staticmethod
    def browser_initialization(config='config.json'):
        """Initialize proper driver/browser.

        Args:
            config(json): file with browser's settings.
        Raises:
            Exception: if unknown browser in config.
        """
        config_browser = os.environ['BROWSER']
        if config_browser not in BrowserFactory.BROWSERS:
            raise Exception(f"Can't initialize {config_browser} driver")
        else:
            if config_browser == 'chrome':                
                ChromeBrowser(config)
            if config_browser == 'firefox':
                FirefoxBrowser(config)
