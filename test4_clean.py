import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from datetime import datetime
from selenium.webdriver import Remote as RemoteWebDriver
from selenium.webdriver.support import expected_conditions as EC

# Import locators
from locators import BasketPageLocators
from locators import CatalogPageLocators
from locators import ProductPageLocators


import time, pytest, urllib, requests

# Exceptions
from selenium.common.exceptions import NoSuchElementException


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
        
        




cataloglink = "http://185.10.185.115:7777/cat/"
cartlink = "http://185.10.185.115:7777/cart/"
product_base_link = "http://185.10.185.115:7777/tour"

duplications = dict()
routeduplicatons = dict()
producturls = []
productlinks = []


#producturls = ["http://185.10.185.115:7777/cat/98", "http://185.10.185.115:7777/cat/99"]



@pytest.mark.parametrize('cataloglink', ["http://185.10.185.115:7777/cat/"])
class TestCatalogPage(object):
    
    #cataloglink = "http://185.10.185.115:7777/cat/"
#---------------------------------------------------------
    
    @pytest.fixture(scope="function", autouse=True) # scope="class" "function"
    def setup(self, browser, cataloglink):
        page = BasePage(browser, cataloglink)
        page.open()
    

    @pytest.mark.skip    
    def test_catalog_product_url_opens(self, browser, cataloglink):  # проверям, что все ссылки на продукты со стр. каталога доступны
        producturls=[]
        
        productlinks = browser.find_elements(*CatalogPageLocators.PRODUCT_DECK) 
      
        for link in productlinks:
            producturls.append(link.get_attribute("href"))
        for counter, url in enumerate(producturls):
            if url == "":
                    print(f"Нет ссылки на карточку продукта {counter}")
            print(url)
            r = requests.get(url)
            if str(r.status_code) != "200":
               print(f"Карточка с продуктом {url} недоступна")        


    @pytest.mark.skip     
    def test_catalog_product_title_exists (self, browser, cataloglink):  # проверям, что все ссылки на продукты со стр. каталога доступны
        producturls=[]
        productlinks = browser.find_elements(*CatalogPageLocators.PRODUCT_DECK)
        for link in productlinks:
            producturls.append(link.get_attribute("href"))
        for url in producturls:
           
            # Заходим на страницу с продуктом, берем превью и проверяем его доступность
            print("Идем в каталог")
          
            browser.implicitly_wait(10)
            browser.get(cataloglink)

            print(f"Открываем url {url}")
            browser.implicitly_wait(10)
            browser.get(url) 

            title = browser.find_element(*ProductPageLocators.PRODUCT_TITLE).text # Ищем заголовок
            print(title)
            if  "404" in title:
                print(f"Страница продукта {url} с наименованием {title} не отображает карточку продукта")

#!!!
    
    @pytest.mark.skip    
    def test_catalog_image_files_opens(self, browser, cataloglink):    
        # Проверям что картинки загружаются
        
        
        
        url_imgs = browser.find_elements(*CatalogPageLocators.PRODUCT_IMAGE_URL)
        assert len(url_imgs) != 0, "Нет ссылок на фото в каталоге!"        
        for link in url_imgs:
            imagelink = link.get_attribute("src")
            if imagelink == None:
                continue
            r = requests.get(imagelink)
            if r.status_code != 200:
               print(f"Неверная ссылка на изображение, {imagelink}")

    @pytest.mark.skip
    def test_catalog_photo_duplication(self, browser, cataloglink):    
        url_imgs = browser.find_elements(*CatalogPageLocators.PRODUCT_IMAGE_URL)
        catduplications=[]
        for link in url_imgs:
            imagelink = link.get_attribute("src")
            if imagelink in duplications:
                print(f"Повтор изображения, {imagelink}")
                


#@pytest.mark.parametrize('link', [f"{product_base_link}/{no}" for no in range(100)])

@pytest.mark.parametrize('link', ["http://185.10.185.115:7777/tour/0"])
class TestBasketPage(object):

    @pytest.fixture(scope="function", autouse=True) # scope="class" "function"
    def setup(self, browser, link):
        browser.implicitly_wait(10)
        #page = BasePage(browser, link)
        #page.open()
        
        # Проверим суммы в корзине
    
    #@pytest.mark.skip 
    
    def test_calc_in_basket(self, browser, link): 
        #def click_all_buttons(css_selector):
        #    assert page.is_element_present(By.CSS_SELECTOR, css_selector), f"Кнопок c CSS,{css_selector} нет"    
        #    buttons = browser.find_elements_by_css_selector(css_selector)        
        #    for button in buttons:
        #        button.click()    
        #        #time.sleep(5)
                
        def click_all_buttons(how, what):
            assert page.is_element_present(how, what), f"Кнопок в {how}, со значением {what} нет"    
            buttons = browser.find_elements(how, what)        
            for button in buttons:
                button.click()    
                #time.sleep(5)        
        def scroll_to_object(how, what):
            assert page.is_element_present(how, what), f"Элемент {how}, со значением {what} не найден"
            scroll_object = browser.find_element(how, what)
            scroll_object.location_once_scrolled_into_view
        def substract_digits_to_string(rawstring):
            digit_list = re.findall(r'[0-9]+', rawstring)
            result = ""
            return (result.join(digit_list))
        def substract_float_digits_to_string(rawstring):
            digit_list = re.findall(r'[0-9.,]+', rawstring)
            result = ""
            return (result.join(digit_list))

#-----------------------------------------in review
        page = BasePage(browser, link)
        page.open()
        
        
        lst=[]
        contents = browser.find_elements(*ProductPageLocators.PRODUCT_PRICE_AND_DATES_TABLE)
        
        # Заготовка массива чтобы проверить даты и суммы
        for t in contents:
            lst.append(t.text)    
        totalprice=0
        for i in range(2, len(lst), 4) :
            #print (f"Price before clean {lst[i]}")
            #price = re.sub("\D", "", lst[i]) #Выдается предупреждение Deprecation Warning
          
            price = substract_float_digits_to_string(lst[i]).replace(",",".")
            
            #print (f"Price after clean {price}")

            totalprice+=float(price)
            #print(price)
        #print("Total price = ",totalprice)
      
        # проматываем до таблицы с ценами 
        scroll_to_object(*ProductPageLocators.PRICE_TABLE)         
        
        # Нажимаем все кнопки купить
        click_all_buttons(*ProductPageLocators.BUY_BUTTONS)

        # Открываем корзину и ищем суммы там

#----------------------- пробуем открыть по нажатию        
        buttonlink = browser.find_element(*ProductPageLocators.BASKET_LINK_ON_PAGE)
        buttonlink.click()        
        
        
        #browser.get(cartlink)         
     
        lst=[]  # Инициализируем список
        contents = browser.find_elements(*ProductPageLocators.PRODUCT_PRICE_AND_DATES_TABLE)
        for t in contents:        # Заготовка массива чтобы проверить суммы
            lst.append(t.text)
        
        totalpriceinbasket=0
        # Суммируем цены в корзине
        for i in range(3, len(lst), 5) :
            #price = re.sub("\D", "", lst[i])  #Выдается предупреждение Deprecation Warning
            price = substract_float_digits_to_string(lst[i]).replace(",",".")
            totalpriceinbasket+=float(price)
            #print(price)
 
        #print("Total price in basket = ",totalpriceinbasket)
        assert round(totalprice,2) == round(totalpriceinbasket,2), "Цены добавленных туров и цены в корзине не совпадают"
        
        # нажимаем все кнопки удалить в корзине
        click_all_buttons(*BasketPageLocators.DELETE_BUTTONS)
        
        # проверяем что корзина пуста
        Empty_basket_tag = browser.find_elements(*BasketPageLocators.EMPTY_BASKET_TAG)  
        # review  - надо делать поддержку разных языков для текста пустой корзины, пока так.
        assert BasketPageLocators.Empty_basket_text in Empty_basket_tag[0].text
        
####  Повторяем покупку чтобы сработал расчет

# нажимаем назад
        browser.back()

        # проматываем до таблицы с ценами 
        scroll_to_object(*ProductPageLocators.PRICE_TABLE)   

        # Нажимаем все кнопки купить
        click_all_buttons(*ProductPageLocators.BUY_BUTTONS)

        #пробуем нажать на линк корзины после покупки
        buttonlink = browser.find_element(*ProductPageLocators.BASKET_LINK_ON_PAGE)
        buttonlink.click()
        
        discount_and_total_price_from_basket = browser.find_elements(*BasketPageLocators.DISCOUNT_AND_PRICE)
        lst=[]
        for t in discount_and_total_price_from_basket:        # Заготовка массива чтобы проверить расчет
            lst.append((t.text).replace(",","."))
            
        discount=float(substract_float_digits_to_string(lst[0])) # Размер скидки на странице
      
        resultt = float(substract_float_digits_to_string(lst[1]))
        totalpricewithdiscount = substract_float_digits_to_string(lst[1]) # Значение Итого на странице продукта

        calculatedpricewithdiscount = round(totalpriceinbasket - totalpriceinbasket*discount/100, 2) #округляем рез-т до 2 знака
    
        assert calculatedpricewithdiscount == totalpricewithdiscount, f"Общая стоимость добавленных туров = {totalpriceinbasket} скидка = {discount} Итого должно быть = {calculatedpricewithdiscount}, а на странице {totalpricewithdiscount}"
        #print(f"Общая стоимость добавленных туров = {totalpriceinbasket} скидка = {discount}% Итого должно быть = {calculatedpricewithdiscount}, а на странице {totalpricewithdiscount}")


        #time.sleep(15)



#@pytest.mark.parametrize('link', [0, 1, 2, 3, 4, 5, 6,pytest.param(7, marks=pytest.mark.xfail),8, 9])


# тесты по определенным номерам продуктов
#numpages=[5,21,25]
#@pytest.mark.parametrize('link', [f"{product_base_link}/{num}" for num in numpages])

# тесты по всем страницам
@pytest.mark.parametrize('link', [f"{product_base_link}/{no}" for no in range(100)])

# тесты по определенным линкам
#@pytest.mark.parametrize('link', ["http://185.10.185.115:7777/tour/21", "http://185.10.185.115:7777/tour/25", "http://185.10.185.115:7777/tour/31", "http://185.10.185.115:7777/tour/33"])


class TestProductPage(object):
    @pytest.fixture(scope="function", autouse=True) # scope="class" "function"
    def setup(self, browser, link):
        page = BasePage(browser, link)
        page.open()
        
    @pytest.mark.skip
    def test_dates_on_product_pages1(self, browser, link):    
        
        lst=[]        
        page = BasePage(browser, link)
        page.open()
        assert page.is_element_present(*ProductPageLocators.PRODUCT_TITLE), "Заголовок продукта не найден"
        contents = browser.find_elements(*ProductPageLocators.PRODUCT_PRICE_AND_DATES_TABLE)
           
        # Заготовка массива чтобы проверить даты и суммы
        for t in contents:
            lst.append(t.text)
        # Проверяем даты начала и конца туров
        for i in range(0, len(lst), 4) :
            startdate = datetime.strptime(str(lst[i]), '%d.%m.%Y')
            enddate = datetime.strptime(str(lst[i+1]), '%d.%m.%Y')
            print(startdate, "---", enddate)
            if startdate == enddate:
                continue
            assert startdate < enddate, "Неверные даты начала и конца тура"

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
                result=list(set(route_list) & set(routeduplicatons[imagelink]))  # Смотрим пересечение обоих списков, если больше однго, то все ОК
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
        


#-----------------------------------
