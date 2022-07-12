from selenium.webdriver.common.by import By
from base.base_form import BaseForm
from base.elements.button_element import Button


class HomePage(BaseForm):
    """Model of 'Home' page."""
    def __init__(self):
        # Locator to some 'unique' page element for page identity
        self.loc_page_marker = (By.XPATH, "//audio[@id='player']")
        self.post_question_button = Button(
            (By.XPATH, "//a[contains(text(), 'Ask a public')]"),
            f'Button to post question form')
        super().__init__()

    def click_ask_public(self):
        """Post question."""
        self.post_question_button.click()        
