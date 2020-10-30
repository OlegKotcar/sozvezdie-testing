from pages.product_page import ProductPage
from pages.catalog_page import CatalogPage
from pages.basket_page import BasketPage

from pages.locators import ProductPageLocators
from pages.locators import BasePageLocators
from pages.locators import BasketPageLocators

from datetime import datetime
from faker import Faker
fake = Faker((['en_US', 'ru_RU']))



import time, pytest, requests

class TestBasketPage(object):
    @pytest.fixture(scope="function", autouse=True) # scope="class" "function"
    def setup(self, browser):
        page = BasketPage(browser, BasePageLocators.CATALOG_LINK)
        page.open()
        
    #@pytest.mark.skip
    def test_dates_on_product_pages(self, browser):    
        page = BasketPage(browser, BasePageLocators.CATALOG_LINK)
        currentproducturl = ""
        
        producturls = page.get_all_product_urls()
        #print(producturls)
        for link in producturls:
            #print(f"Открываем вкладку с {link}")
            currentproducturl = link
            browser.implicitly_wait(10)
            browser.execute_script(f"window.open('{link}')") # открываем новую вкладку с продуктом
            browser.switch_to.window(browser.window_handles[1]) # переходим на новую вкладку
          
            # Тут все делаем на странице
     
            totalpriceelement = browser.find_elements(*ProductPageLocators.PRODUCT_PRICE_COLUMN)
            totalprice =  sum([float(page.substract_float_digits_to_string(totalpriceelement[x].text)) for x in range (len(totalpriceelement))])

            # Проверяем есть ли вообще стоимость туров на странице продукта, если пусто => следующая итерация
            if totalprice <=0:
                print(f"На странице {currentproducturl} нет предложений по ценам")
                browser.close() # закрываем _ВКЛАДКУ_
                browser.switch_to.window(browser.window_handles[0]) # переключаемся на первую вкладку
                continue
            
            # проматываем до таблицы с ценами 
            page.scroll_to_object(*ProductPageLocators.PRICE_TABLE)         
        
            # Нажимаем все кнопки купить
            page.click_all_buttons(*ProductPageLocators.BUY_BUTTONS)

           # Открываем корзину и ищем суммы там
            buttonlink = browser.find_element(*ProductPageLocators.BASKET_LINK_ON_PAGE) 
            buttonlink.click()   #- пробуем открыть по нажатию на ссылку    
        
        
            #browser.get(cartlink)         
     
            totalpriceinbasketelement = browser.find_elements(*BasketPageLocators.PRODUCT_PRICE_BASKET_COLUMN)
            totalpriceinbasket =  sum([float(page.substract_float_digits_to_string(totalpriceinbasketelement[x].text)) for x in range (len(totalpriceinbasketelement))])
            
            print(totalpriceinbasket)
            
            #print("Общая стоимость всех предложений, добавленных в корзину = ",totalpriceinbasket)
            assert round(totalprice,2) == round(totalpriceinbasket,2), f"В продукте по ссылке {currentproducturl} цены добавленных туров и цены в корзине не совпадают"
        
            # нажимаем все кнопки удалить в корзине
            page.click_all_buttons(*BasketPageLocators.DELETE_BUTTONS)
        
            # проверяем что корзина пуста
            page.should_be_empty_basket()
        
####  Повторяем покупку чтобы сработал расчет

            # нажимаем назад
            browser.back()

            # проматываем до таблицы с ценами 
            page.scroll_to_object(*ProductPageLocators.PRICE_TABLE)   

            # Нажимаем все кнопки купить
            page.click_all_buttons(*ProductPageLocators.BUY_BUTTONS)

            #пробуем нажать на линк корзины после покупки
            buttonlink = browser.find_element(*ProductPageLocators.BASKET_LINK_ON_PAGE)
            buttonlink.click()
            
            discountelement = browser.find_element(*BasketPageLocators.DISCOUNT).text
            totalpriceelement = browser.find_element(*BasketPageLocators.TOTALPRICE).text
            
            discount=float(page.substract_float_digits_to_string(discountelement)) # Размер скидки на странице
            #print(discount)

            totalpricewithdiscount = round(float(page.substract_float_digits_to_string(totalpriceelement)),2)
            calculatedpricewithdiscount = round(totalpriceinbasket - totalpriceinbasket*discount/100, 2) #округляем рез-т до 2 знака
    
            #assert calculatedpricewithdiscount == totalpricewithdiscount, f"Общая стоимость добавленных туров = {totalpriceinbasket} скидка = {discount} Итого должно быть = {calculatedpricewithdiscount}, а на странице {totalpricewithdiscount}"
            print(f"Общая стоимость добавленных туров на странице продукта {currentproducturl} равна {totalpriceinbasket} скидка = {discount}% Итого должно быть = {calculatedpricewithdiscount}, а на странице {totalpricewithdiscount}")

#----------------------------------------------------------------------

            # проматываем в начало страницы
            #page.scroll_to_object(*BasketPageLocators.DISCOUNT_AND_PRICE)    
            browser.execute_script("window.scroll(0, 0);")
 
            # нажимаем все кнопки удалить в корзине
            page.click_all_buttons(*BasketPageLocators.DELETE_BUTTONS)
        
            # проверяем что корзина пуста
            page.should_be_empty_basket()           
            
#------------------------------------------------------            
            browser.close() # закрываем _ВКЛАДКУ_
            #time.sleep(10)
            browser.switch_to.window(browser.window_handles[0]) # переключаемся на первую вкладку

    
    @pytest.mark.skip
    def test_payment_in_basket(self, browser): 

#   review  Пока ссылки прямые, бео локаторов
        #print(fake.text(255))
        
        link = "http://185.10.185.115:7777/tour/3"          
        cartlink = "http://185.10.185.115:7777/cart/"
        
        page = BasketPage(browser, link)
        page.open()
        
        # проматываем до таблицы с ценами 
        page.scroll_to_object(*ProductPageLocators.PRICE_TABLE)         
        
        # Нажимаем все кнопки купить
        page.click_all_buttons(*ProductPageLocators.BUY_BUTTONS)

        # Открываем корзину 
        buttonlink = browser.find_element(*ProductPageLocators.BASKET_LINK_ON_PAGE)
        buttonlink.click()        
        
        browser.get(cartlink)
        
        name = browser.find_element(*BasketPageLocators.NAME_FIELD)
        email = browser.find_element(*BasketPageLocators.EMAIL_FIELD)
        password = browser.find_element(*BasketPageLocators.PASSWORD_FIELD)
        cardnumber = browser.find_element(*BasketPageLocators.CARDNUMBER_FIELD)
        cardholder = browser.find_element(*BasketPageLocators.CARDHOLDER_FIELD)
        expdate = browser.find_element(*BasketPageLocators.EXPDATE_FIELD)
        cvccode = browser.find_element(*BasketPageLocators.CVCCODE_FIELD)
        
        cardnumber.send_keys("aaaabbbbccccdddd")
        #cardnumber.send_keys("1111222233334444") 
        
        # Нажимаем оплатить
        browser.find_element(*BasketPageLocators.PAYBUTTON).click()
        

        validation_message = cardnumber.get_attribute("validationMessage");
       
        if validation_message == "" :
            print("Не Видно")
        else:
            print("Видно!")   
        
        #time.sleep(15)
        
        #assert not WebDriverWait(browser, 5).until(EC.element_located_to_be_selected((By.XPATH, "//input [@id='cardName']/following-sibling::div[@class='invalid-feedback']"))), "Неверный ввод имени на карте"
        #time.sleep(10)
        
        cardnumber.clear()
        cardnumber.send_keys(u'\ue009' + u'\ue003')     
        cardnumber.send_keys("1111222233334444") # "правильные значения"
  
       
        validation_message = cardnumber.get_attribute("validationMessage");
    
        if validation_message == "" :
            print("Подсказки об ошибке нет")
        else:
            print("Есть подсказка об ошибке")        
        
        
        
        time.sleep(5)
        
