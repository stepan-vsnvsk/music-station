from selenium.webdriver.common.by import By
from base.base_form import BaseForm


class LoginPage(BaseForm):
    """Model of 'Login' page."""
    def __init__(self):
        # Locator to some 'unique' page element for page identity        
        self.loc_page_marker = (By.XPATH, "//input[@name='username']")
        super().__init__()
