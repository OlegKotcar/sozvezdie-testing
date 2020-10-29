from selenium.webdriver.common.by import By


class BasePageLocators():
    MAIN_LINK = "http://185.10.185.115:7777/"
    CATALOG_LINK = "http://185.10.185.115:7777/cat"
    BASKET_LINK = "http://185.10.185.115:7777/cart"
    #CATALOG_LINK = (By.find_element_by_partial_link_text, "cat")
    #BASKET_LINK = (By.find_element_by_partial_link_text, "cart")
    #PRODUCT_IMAGE_URL = (By.CSS_SELECTOR, "div.catalog.card-deck img") #Ссылки на изображения (превью) всех продуктов в каталоге



class CatalogPageLocators():
    PRODUCT_DECK = (By.CSS_SELECTOR,".catalog.card-deck a") # Ссылки на все продукты со страницы каталога
    PRODUCT_IMAGE_URL = (By.CSS_SELECTOR, "div.catalog.card-deck img") #Ссылки на изображения (превью) всех продуктов в каталоге
    PRODUCT_PREVIEW = (By.CSS_SELECTOR, ".card-img-top") #блок для картинки превью в каталоге


class ProductPageLocators():
    PRODUCT_TITLE = (By.CSS_SELECTOR, "#page-content div h1") #Заголовок на странице продукта ! можно короче .col > h1
    PRODUCT_PRICE_AND_DATES_TABLE = (By.CSS_SELECTOR, "tr td")  #Таблица на странице продукта с датами и ценами
    BUY_BUTTONS = (By.CSS_SELECTOR, "button.btn") # Кнопки купить на странице продукта
    PRICE_TABLE = (By.CSS_SELECTOR, ".table.price-table") # Таблици с ценами для позиционирования
    BASKET_LINK_ON_PAGE = (By.CSS_SELECTOR, "td a") # Ссылка на корзину на странице продукта после нажатия кнопки купить
    PRODUCT_THUMBNAIL = (By.CSS_SELECTOR, "div>img.photo-card") # Ссылка на превью на станице продукта
    PHOTO_GALLERY = (By.CSS_SELECTOR, "div.react-photo-gallery--gallery img")
    ROUTE = (By.XPATH, "//div[@class='text-center']/p") # Текст маршрута на странице продукта
    

class BasketPageLocators():
    Empty_basket_text = "Корзина пуста" #review  - надо делать поддержку разных языков для текста пустой корзины, пока так.
    DELETE_BUTTONS = (By.CSS_SELECTOR, "button.btn.btn-outline-danger") # Кнопки удалить в корзине
    EMPTY_BASKET_TAG = (By.CSS_SELECTOR, "div.alert-info") # Сообщение о пустой корзине
    DISCOUNT_AND_PRICE = (By.CSS_SELECTOR, "tfoot tr td")
    PAYBUTTON = (By.XPATH, "//*[@type='submit']") # кнопка оплатить
    NAME_FIELD = (By.CSS_SELECTOR, "#name")
    EMAIL_FIELD = (By.CSS_SELECTOR, "#email")
    PASSWORD_FIELD = (By.CSS_SELECTOR, "#password")
    CARDNUMBER_FIELD = (By.CSS_SELECTOR, "#cardNumber")
    CARDHOLDER_FIELD = (By.CSS_SELECTOR, "#cardName")
    EXPDATE_FIELD = (By.CSS_SELECTOR, "#cardExpiry")
    CVCCODE_FIELD = (By.CSS_SELECTOR, "#cardCvc")





#    CARDNAMEERROR = (By.XPATH, "//input [@id='cardName']") # Неверное имя на карте
#    CARDNUMBERERROR = (By.XPATH, "//input [@id='cardNumber']")  # Неверный номер карты
#    EXPDATEERROR = (By.XPATH, "//input [@id='cardExpiry']") # Неверная дата окончания
#    CVCCODEERROR = (By.XPATH, "//input [@id='cardCvc']") # Неверный CVC код

#XPATH
#//input [@id='cardName']/following-sibling::div[@class='invalid-feedback']") # Неверное имя на карте
#"//input [@id='cardNumber']/following-sibling::div[@class='invalid-feedback']" # неверный номер карты
#//input [@id='cardExpiry']/following-sibling::div[@class='invalid-feedback']") # Неверная дата окончания
#"//input [@id='cardCvc']/following-sibling::div[@class='invalid-feedback']") # Неверный CVC код
