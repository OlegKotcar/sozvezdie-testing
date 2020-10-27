from pages.catalog_page import CatalogPage
from pages.locators import CatalogPageLocators
from pages.locators import BasePageLocators

import time, pytest, requests




class TestCatalogPage(object):
#---------------------------------------------------------
    #producturls=["http://185.10.185.115:7777/tour/0"]
   
    @pytest.fixture(scope="function", autouse=True) # scope="class" "function"
    def setup(self, browser):
        page = CatalogPage(browser, BasePageLocators.CATALOG_LINK)
        page.open()
    
    #@pytest.mark.skip 
    def test_catalog_image_files_exist_and_opens(self, browser):    
        page = CatalogPage(browser, BasePageLocators.CATALOG_LINK)
        
        duplications=dict()
        
        page.catalog_image_is_not_empty()
        preview_urls = browser.find_elements(*CatalogPageLocators.PRODUCT_PREVIEW)

# Проверяем есть ли дубликаты картинок на разных продуктах
        for counter, link in enumerate(preview_urls):
            imagelink = link.get_attribute("src")        
            if imagelink not in duplications:
                duplications[imagelink] = [counter]
            else:
                duplications[imagelink].append(counter)
        for key, value in duplications.items():
            if len(value) > 1:
                print(f"Изображение {key}, повторяется в продуктах с порядковыми номерами {value}")       

#        print(duplications)


# Проверяем содержат ли продукты превью и правлиьные ли ссылки на них
        for counter, link in enumerate(preview_urls):
            imagelink = link.get_attribute("src")
            if imagelink == None:
                 print(f"Продукт с порядковым номером {counter} не содержит картинки превью")
            else:
                r = requests.get(imagelink)
                if r.status_code != 200:
                    print(f"На странице с порядковым номером {counter} неверная ссылка на изображение, {imagelink} ")
              


    
    @pytest.mark.skip 
    #@pytest.mark.parametrize('link', link)    
    def test_open_product_url_in_new_bowser_window(self, browser):
        page = CatalogPage(browser, BasePageLocators.CATALOG_LINK)
        page.open()        

        producturls = page.get_all_product_urls()
        
        #producturls=["http://185.10.185.115:7777/tour/0", "http://185.10.185.115:7777/tour/98", "http://185.10.185.115:7777/tour/99"]

        #print(producturls)
        
        for link in producturls:
            #print(f"Открываем вкладку с {link}")
            browser.implicitly_wait(10)
            browser.execute_script(f"window.open('{link}')") # открываем новую вкладку с продуктом
            browser.switch_to.window(browser.window_handles[1]) # переходим на новую вкладку
            page.should_be_title_for_product() # На вкладке должно быть название
            
            browser.close() # закрываем _ВКЛАДКУ_
       
            #time.sleep(10)
            browser.switch_to.window(browser.window_handles[0]) # переключаемся на первую вкладку
        
    
    @pytest.mark.skip 
    def test_catalog_product_url_opens(self, browser):  # проверям, что все ссылки на продукты со стр. каталога доступны
        page = CatalogPage(browser, BasePageLocators.CATALOG_LINK)
        page.open()

  
        producturls=[]
        productlinks = browser.find_elements(*CatalogPageLocators.PRODUCT_DECK) # Выбираем все ссылки в каталоге
        for link in productlinks:
            producturls.append(link.get_attribute("href"))
        
        #print(producturls)

     
        for counter, url in enumerate(producturls):
            if url == "":
                    print(f"Нет ссылки на карточку продукта {counter}")
            print(url)
            r = requests.get(url)
            if str(r.status_code) != "200":
               print(f"Карточка с продуктом {url} недоступна")        
            
            print("Пробуем открывать в браузере")
            browser.get(url)    # Пробуем открывать карточку продукта в браузере
            page.should_be_title_for_product()
            
   
