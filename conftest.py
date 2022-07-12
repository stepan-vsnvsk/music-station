import pytest
from driver.singletone import Singletone
from driver.browser_factory import BrowserFactory
from util.logger import Logger


@pytest.fixture(scope='class', autouse=True)
def driver_init():
    """Driver initialization.

    Setup: Call proper browser/driver.
    Teardown: Quit browser, clear Singletone.
    """
    BrowserFactory.browser_initialization()
    browser = Singletone.get_instance() 
    browser.driver.maximize_window()   
    yield
    browser.driver.quit()
    Singletone._instance = None


@pytest.fixture(autouse=True)
def log(request):
    """Logging initialization."""
    test_name = request.node.name
    Logger().set_file_handler(test_name)   
    yield 
