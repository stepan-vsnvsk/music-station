from pages.home_page import HomePage
from pages.login_page import LoginPage 
from driver.driver_util import DriverUtil
from util.config_manager import ConfigManager
from util.logger import Logger as log


def test_post_question_unauthorised():
    log.info("Test case 'Post quesiton as unauthorised user' is started")            
    log.info("Step 1: Navigate to home page")
    url = ConfigManager.get_value_from_config('URL')        
    home_page = HomePage()        
    driver_util = DriverUtil()       
    driver_util.navigate_to(url)
    driver_util.screenshot('home_page')        
    assert home_page.is_page_open(), \
        "Can't open Main page " \
        "Expected result: Home page is open."

    log.info("Step 2: Click the 'Ask public' button.")
    home_page.click_ask_public()    
    login_page = LoginPage()
    driver_util.screenshot('login_page')  
    assert login_page.is_page_open(), \
        "Can't open 'Login' page' " \
        "Expected result: Login page is opened"
