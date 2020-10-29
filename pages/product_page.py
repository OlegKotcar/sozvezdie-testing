from .base_page import BasePage
from .locators import CatalogPageLocators
from .locators import ProductPageLocators

import time, pytest



class ProductPage(BasePage):
    
   
 
    def should_be_title_for_product (self):  # проверям, что все ссылки на продукты со стр. каталога доступны
        if not self.is_element_present(*ProductPageLocators.PRODUCT_TITLE):
            print(f"Страница продукта {self.browser.current_url} не содержит заголовка")
        
        else:     
            title = self.browser.find_element(*ProductPageLocators.PRODUCT_TITLE).text # Ищем заголовок
            assert "404" not in title, f"Страница продукта {self.browser.current_url} с заголовком {title} не отображает карточку продукта"
        
        #assert self.is_element_present(*ProductPageLocators.PRODUCT_TITLE), f"Страница продукта {self.browser.current_url} не содержит заголовка"

    def should_be_thumb_for_product (self):  # проверям, что все ссылки на продукты со стр. каталога доступны
        result = True
        if not self.is_element_present(*ProductPageLocators.PRODUCT_THUMBNAIL):
            print(f"Страница продукта {self.browser.current_url} не содержит фото превью")
            result = False
        return(result)


    def should_be_photoalbum_for_product (self):  # проверям, что все ссылки на продукты со стр. каталога доступны
        result = True
        if not self.is_element_present(*ProductPageLocators.PHOTO_GALLERY):
            print(f"Страница продукта {self.browser.current_url} не содержит блока Фотоальбом")
            result = False
        return(result)

    def should_be_route_for_product (self):  # проверям, что на странице есть маршрут
        result = True
        if not self.is_element_present(*ProductPageLocators.ROUTE):
            print(f"Страница продукта {self.browser.current_url} не содержит блока маршрут")
            result = False
        return(result)


    def catalog_image_is_not_empty(self):    
        url_imgs = self.browser.find_elements(*CatalogPageLocators.PRODUCT_IMAGE_URL)
        if len(url_imgs) == 0:
            print(f"Нет ссылок на фото в каталоге продуктов!")
            return False
        else:
            return True
        #assert len(url_imgs) != 0, "Нет ссылок на фото в каталоге!"        


               
