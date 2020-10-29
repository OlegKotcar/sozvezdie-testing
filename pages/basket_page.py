from .base_page import BasePage
from .locators import CatalogPageLocators
from .locators import ProductPageLocators
from .locators import BasketPageLocators

import time, pytest, re



class BasketPage(BasePage):
   
    def substract_digits_to_string(self, rawstring):
        digit_list = re.findall(r'[0-9]+', rawstring)
        result = ""
        return (result.join(digit_list))
    
    def substract_float_digits_to_string(self, rawstring):
        digit_list = re.findall(r'[0-9.,]+', rawstring)
        result = ""
        return (result.join(digit_list).replace(",","."))   

    def should_be_empty_basket (self):  # проверям, что корзина пустая
        Empty_basket_tag = self.browser.find_elements(*BasketPageLocators.EMPTY_BASKET_TAG)  
            # review  - надо делать поддержку разных языков для текста пустой корзины, пока так. см. locators
        assert BasketPageLocators.Empty_basket_text in Empty_basket_tag[0].text
    