from selenium.webdriver import Remote as RemoteWebDriver

# Import Exceptions
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException

# Locators
from pages.locators import CatalogPageLocators
from pages.locators import BasePageLocators


class BasePage():
    def __init__(self, browser: RemoteWebDriver, url, timeout=10):
        #def __init__(self, browser, url):
        self.browser = browser
        self.url = url
        self.browser.implicitly_wait(timeout)

    def open(self):
        self.browser.get(self.url)
        
    def is_element_present(self, how, what):
        try:
            self.browser.find_element(how, what)
        except (NoSuchElementException):
            return False
        return True
    
    def scroll_to_object(self, css_object):
        self.browser.execute_script("return arguments[0].scrollIntoView(true);", css_object)
        #time.sleep(10)
    
    def go_to_mainpage(self):
        link = self.browser.find_element(BasePageLocators.MAIN_LINK)
        link.click()    
    
    def go_to_catalog(self):
        link = self.browser.find_element(BasePageLocators.CATALOG_LINK)
        link.click()
    
    def go_to_basket(self):
        link = self.browser.find_element(BasePageLocators.BASKET_LINK)
        link.click()
    