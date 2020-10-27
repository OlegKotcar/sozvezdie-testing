from pages.product_page import ProductPage
from pages.catalog_page import CatalogPage

from pages.locators import ProductPageLocators
from pages.locators import BasePageLocators

from datetime import datetime

#datetime.datetime.strptime

import pytest

class TestProductPage(object):
    #producturls=["http://185.10.185.115:7777/tour/0"]

    
    
    @pytest.fixture(scope="function", autouse=True) # scope="class" "function"
    def setup(self, browser):
        page = ProductPage(browser, BasePageLocators.CATALOG_LINK)
        page.open()
        
    #@pytest.mark.skip
    def test_dates_on_product_pages(self, browser):    
        page = CatalogPage(browser, BasePageLocators.CATALOG_LINK)
        
        producturls = page.get_all_product_urls()
        #print(producturls)
        for link in producturls:
            #print(f"Открываем вкладку с {link}")
            browser.implicitly_wait(10)
            browser.execute_script(f"window.open('{link}')") # открываем новую вкладку с продуктом
            browser.switch_to.window(browser.window_handles[1]) # переходим на новую вкладку
            
            
            # Тут все делаем на странице
            
            lst=[]
            contents = browser.find_elements(*ProductPageLocators.PRODUCT_PRICE_AND_DATES_TABLE)
            
            # Заготовка массива чтобы проверить даты и суммы
            for t in contents:
                lst.append(t.text)
            
            #print(lst)
            
            for i in range(0, len(lst), 4) :
                startdate = datetime.strptime(str(lst[i]), '%d.%m.%Y')
                enddate = datetime.strptime(str(lst[i+1]), '%d.%m.%Y')
                print(startdate, "---", enddate)
                if startdate == enddate:
                    continue
                assert startdate < enddate, "Неверные даты начала и конца тура"
            
            
            browser.close() # закрываем _ВКЛАДКУ_
       
            #time.sleep(10)
            browser.switch_to.window(browser.window_handles[0]) # переключаемся на первую вкладку
        
        
        
                
        
        
        
           

        # Проверяем даты начала и конца туров


    @pytest.mark.skip
    def test_check_photoalbum_load_images(self, browser, link):    
     
        # Проверям что картинки (превью) загружаются
        url_img = browser.find_element(*ProductPageLocators.PRODUCT_THUMBNAIL).get_attribute("src")
        #print(url_img)
        r = requests.get(url_img)
        assert r.status_code == 200, f"Неверная ссылка на изображение{url_img}"
    
    @pytest.mark.skip
    def test_photoalbum_load_image_files(self, browser, link):    
      
        # Проверям что картинки загружаются
        ##url_imgs = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.react-photo-gallery--gallery img")))
        
        url_imgs = browser.find_elements(*ProductPageLocators.PHOTO_GALLERY)
        
        assert len(url_imgs) != 0, f"Нет фотоальбома или фотографий в фотоальбоме, {browser.current_url}"        
        
        for link in url_imgs:
            imagelink = link.get_attribute("src")
            r = requests.get(imagelink)
            assert r.status_code == 200, f"Неверная ссылка на изображение, {imagelink}, в фотоальбоме {browser.current_url}"

   
    @pytest.mark.skip
    def test_photoalbum_photo_files_duplication(self, browser, link):    
        url_imgs = browser.find_elements(*ProductPageLocators.PHOTO_GALLERY)
        assert len(url_imgs) != 0, f"Нет фотоальбома или фотографий в фотоальбоме, {browser.current_url}"        
        route = browser.find_element(*ProductPageLocators.ROUTE)
        route_list=route.text.replace(" ", "").split("-")

        for link in url_imgs:
            imagelink = link.get_attribute("src")
            if imagelink not in duplications:  # если url картинки нет в словаре то добавляем маршрут и ссылку на продук              
                duplications[imagelink] = [browser.current_url]
                routeduplicatons[imagelink] = route_list
            else: # если url картинки уже есть, смотрим есть ли она в маршруте
                result=list(set(route_list) & set(routeduplicatons[imagelink]))  # Смотрим пересечение обоих списков, если больше однго, то все ОК. Это может пригодиться в дальнейшем анализе маршрута. Можно применить set.intersection
                
                #print(result)
                if len(result) >= 0:  #  Если есть совпадение, то идем к след. картинке
                    continue
                else: # если нет пересечений, то добавляем url продукта к картинке
                    duplications[imagelink].append(browser.current_url)

        # Печатаем все совпадения, если их больше 1 - картинка найдена на разных маршуртах более 1 раза
        #print(duplications)
  
        for key, value in duplications.items():
            if len(value) > 1:
                print(key, value)
        
