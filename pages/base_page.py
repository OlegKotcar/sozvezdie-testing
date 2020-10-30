from selenium.webdriver import Remote as RemoteWebDriver

# Import Exceptions
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException

# Locators
from pages.locators import CatalogPageLocators
from pages.locators import BasePageLocators

from datetime import datetime


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
    
#    def scroll_to_object(self, css_object):
#        self.browser.execute_script("return arguments[0].scrollIntoView(true);", css_object)
 

    def scroll_to_object(self, how, what):
        assert self.is_element_present(how, what), f"Элемент {how}, со значением {what} не найден"
        scroll_object = self.browser.find_element(how, what)
        scroll_object.location_once_scrolled_into_view     
        
    
    def go_to_mainpage(self):
        link = self.browser.find_element(BasePageLocators.MAIN_LINK)
        link.click()    
    
    def go_to_catalog(self):
        link = self.browser.find_element(BasePageLocators.CATALOG_LINK)
        link.click()
    
    def go_to_basket(self):
        link = self.browser.find_element(BasePageLocators.BASKET_LINK)
        link.click()
    
    def get_all_product_urls(self):
        producturls=[]
        productlinks = self.browser.find_elements(*CatalogPageLocators.PRODUCT_DECK) # Выбираем все ссылки в каталоге
        for link in productlinks:
            producturls.append(link.get_attribute("href"))    
        return(producturls)    
   
    def convert_string_to_date(self, rawstring):
        result = datetime.strptime(rawstring,BasePageLocators.DATE_CONVERT_TEMPLATE).date()
        return result
   
   
        
    def click_all_buttons(self, how, what):
        assert self.is_element_present(how, what), f"Кнопок в {how}, со значением {what} нет"    
        buttons = self.browser.find_elements(how, what)        
        for button in buttons:
            button.click()    
            #time.sleep(5)                