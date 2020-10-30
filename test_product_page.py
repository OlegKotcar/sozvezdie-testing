from pages.product_page import ProductPage
from pages.catalog_page import CatalogPage

from pages.locators import ProductPageLocators
from pages.locators import BasePageLocators
from pages.locators import CatalogPageLocators

from datetime import datetime

import pytest, requests

class TestProductPage(object):
    #producturls=["http://185.10.185.115:7777/tour/0"]
    
    @pytest.fixture(scope="function", autouse=True) # scope="class" "function"
    def setup(self, browser):
        page = ProductPage(browser, BasePageLocators.CATALOG_LINK)
        page.open()
        
    #@pytest.mark.skip
    def test_dates_on_product_pages(self, browser):    
        page = ProductPage(browser, BasePageLocators.CATALOG_LINK)
        
        producturls = page.get_all_product_urls()
        catalog_product_dates = browser.find_elements(*CatalogPageLocators.PRODUCT_DATE)
        
        preview_dates = [catalog_product_dates[x].text for x in range (0, len(catalog_product_dates))]
        #print(preview_dates)

        for numproduct, link in enumerate(producturls):
            #print(f"Открываем вкладку с {link}")
            browser.implicitly_wait(10)
            browser.execute_script(f"window.open('{link}')") # открываем новую вкладку с продуктом
            browser.switch_to.window(browser.window_handles[1]) # переходим на новую вкладку

            # Тут все делаем на странице
            
            preview_dates_range = preview_dates[numproduct].split(BasePageLocators.DATE_SPLIT_SYMBOL)
            #print(preview_dates_range)
            
            if preview_dates_range[0] == '':
                print(f"Для продукта {link} на странице каталога нет ближайших дат его начала")
                startdateincatalog = ''
                enddateincatalog = ''
            else:
                startdateincatalog = page.convert_string_to_date(preview_dates_range[0])
                enddateincatalog = page.convert_string_to_date(preview_dates_range[1])
            
            if not page.should_be_price_date_for_product():
                print(f"страница продукта {link} не содержит блока дат и цен")

            startdateselement = browser.find_elements(*ProductPageLocators.PRODUCT_START_DATE_COLUMN) 
            enddateselement = browser.find_elements(*ProductPageLocators.PRODUCT_END_DATE_COLUMN) 

            allstartdates = [startdateselement[x].text for x in range (len(startdateselement))]
            allenddates = [enddateselement[x].text for x in range (len(enddateselement))]
            nowdate = datetime.now().date()
            
            if len(allstartdates) > 0:
                earliestdate = (page.convert_string_to_date(min(allstartdates))) 
            else:
                earliestdate = ""  
            #print(earliestdate)
             
            for i in range(0, len(allstartdates)):
                startdate = page.convert_string_to_date(allstartdates[i])
                enddate = page.convert_string_to_date(allenddates[i])
            # Сразу проверяем совпадает ли ближайшая дата с датой в каталоге (список отсортирован)
                if i ==0 and startdateincatalog != earliestdate:
                    print(f"В каталоге для продукта {link}  указана ближайшая дата {startdateincatalog}, ближайшая дата на стр. {earliestdate}") 
            # Дальше проверяем на начало < конца и текущую дату
                if startdate < nowdate:            
                    print(f"На странице продукта {link} начало тура {startdate} позднее текущей даты {nowdate}") 

#                if startdate == enddate:
#                    continue    # тут аккуратно, надо не забывать про открытые вкладки

                if startdate > enddate:
                    print(f"Неверные даты начала {startdate} и конца тура {enddate}")
  
            browser.close() # закрываем _ВКЛАДКУ_
            #time.sleep(10)
            browser.switch_to.window(browser.window_handles[0]) # переключаемся на первую вкладку
       



    @pytest.mark.skip
    def test_product_thumbs(self, browser):    
        
        page = ProductPage(browser, BasePageLocators.CATALOG_LINK)
        producturls = page.get_all_product_urls()
        #print(producturls)

        for link in producturls:
            #print(f"Открываем вкладку с {link}")
            browser.implicitly_wait(10)
            browser.execute_script(f"window.open('{link}')") # открываем новую вкладку с продуктом
            browser.switch_to.window(browser.window_handles[1]) # переходим на новую вкладку
          
            # Тут все делаем на странице    
            
            if not page.should_be_thumb_for_product(): # На странице продукта должно быть превью
                browser.close()
                browser.switch_to.window(browser.window_handles[0])
                continue
            else:
                url_img = browser.find_element(*ProductPageLocators.PRODUCT_THUMBNAIL).get_attribute("src")
                #print(url_img)
                r = requests.get(url_img)
                if r.status_code != 200:
                    print(f"Неверная ссылка на изображение {url_img} в продукте со ссылкой {browser.current_url}")
  

  
            browser.close() # закрываем _ВКЛАДКУ_
            browser.switch_to.window(browser.window_handles[0]) # переключаемся на первую вкладку
     
# Проверяем фотоальбом

    
    @pytest.mark.skip
    def test_photoalbum_load_image_files(self, browser):    
        page = ProductPage(browser, BasePageLocators.CATALOG_LINK)
        producturls = page.get_all_product_urls()
        #print(producturls)

        for link in producturls:
            #print(f"Открываем вкладку с {link}")
            browser.implicitly_wait(10)
            browser.execute_script(f"window.open('{link}')") # открываем новую вкладку с продуктом
            browser.switch_to.window(browser.window_handles[1]) # переходим на новую вкладку
          
            # Тут все делаем на странице    
            
            
            if not page.should_be_photoalbum_for_product(): # На странице продукта должен быть фотоальбом
                browser.close()
                browser.switch_to.window(browser.window_handles[0])
                continue
            else:
                url_imgs = browser.find_elements(*ProductPageLocators.PHOTO_GALLERY)
                if len(url_imgs) > 0: 
                    for url_img in url_imgs:
                        imagelink = url_img.get_attribute("src")
                        r = requests.get(imagelink)
                        if r.status_code != 200:
                             print(f"Неверная ссылка на изображение {imagelink} в Фотоальбоме продукта со ссылкой {browser.current_url}")
                else:    
                    print(f"Блок Фотоальбом есть, но нет фотографий в продукте {browser.current_url}")
                #print(url_img)

  
            browser.close() # закрываем _ВКЛАДКУ_
            browser.switch_to.window(browser.window_handles[0]) # переключаемся на первую вкладку


   
    @pytest.mark.skip
    def test_photoalbum_photo_files_duplication(self, browser):    
        page = ProductPage(browser, BasePageLocators.CATALOG_LINK)
        producturls = page.get_all_product_urls()
 
        duplications = dict()
        routeduplicatons = dict()

        for link in producturls:
            #print(f"Открываем вкладку с {link}")
            browser.implicitly_wait(10)
            browser.execute_script(f"window.open('{link}')") # открываем новую вкладку с продуктом
            browser.switch_to.window(browser.window_handles[1]) # переходим на новую вкладку
          
            # Тут все делаем на странице  
            if not (page.should_be_photoalbum_for_product() and page.should_be_route_for_product): # На странице продукта должен быть фотоальбом и маршрут для этого теста
                browser.close()
                browser.switch_to.window(browser.window_handles[0])
                continue
            else:
                route = browser.find_element(*ProductPageLocators.ROUTE)
                route_list=route.text.replace(" ", "").split("-")
                #print(route_list)
                url_imgs = browser.find_elements(*ProductPageLocators.PHOTO_GALLERY)
                for link in url_imgs:
                    imagelink = link.get_attribute("src")
                    if imagelink not in duplications:  # если url картинки нет в словаре то добавляем маршрут и ссылку на продук              
                        duplications[imagelink] = [browser.current_url]
                        routeduplicatons[imagelink] = route_list
                    else: # если url картинки уже есть, смотрим есть ли она в маршруте
                        result=list(set(route_list) & set(routeduplicatons[imagelink]))  # Смотрим пересечение обоих списков, если больше однго, то все ОК. Это может пригодиться в дальнейшем анализе маршрута. Можно применить set.intersection
                
                        #print(result)
                        if len(result) == 0:  #  Если совпадений нет, то добавляем дубликат
                            duplications[imagelink].append(browser.current_url)

            browser.close() # закрываем _ВКЛАДКУ_
            browser.switch_to.window(browser.window_handles[0]) # переключаемся на первую вкладку

        # Печатаем все совпадения, если их больше 1 - картинка найдена на разных маршуртах более 1 раза
        #print(duplications)
  
        for key, value in duplications.items():
            if len(value) > 1:
                print(key, value)
    
        print("Проверка закончена") 


        
