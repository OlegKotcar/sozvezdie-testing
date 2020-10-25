from selenium.webdriver.common.by import By


class CatalogPageLocators():
    PRODUCT_DECK = (By.CSS_SELECTOR,".catalog.card-deck a") # Ссылки на все продукты со страницы каталога
    PRODUCT_IMAGE_URL = (By.CSS_SELECTOR, "div.catalog.card-deck img") #Ссылки на изображения (превью) всех продуктов в каталоге


class ProductPageLocators():
    PRODUCT_TITLE = (By.CSS_SELECTOR, "#page-content div h1") #Заголовок на странице продукта
    PRODUCT_PRICE_AND_DATES_TABLE = (By.CSS_SELECTOR, "tr td")  #Таблица на странице продукта с датами и ценами
    BUY_BUTTONS = (By.CSS_SELECTOR, "button.btn") # Кнопки купить на странице продукта
    PRICE_TABLE = (By.CSS_SELECTOR, ".table.price-table") # Таблици с ценами для позиционирования
    BASKET_LINK_ON_PAGE = (By.CSS_SELECTOR, "td a") # Ссылка на корзину на странице продукта после нажатия кнопки купить
    PRODUCT_THUMBNAIL = (By.CSS_SELECTOR, "div>img.photo-card") # Ссылка на превью на станице продукта
    PHOTO_GALLERY = (By.CSS_SELECTOR, "div.react-photo-gallery--gallery img")
    ROUTE = (By.XPATH , "//div[@class='text-center']/p") # Текст маршрута на странице продукта
    
 




class BasketPageLocators():
    DELETE_BUTTONS = (By.CSS_SELECTOR, "button.btn.btn-outline-danger") # Кнопки удалить в корзине


    
    
    
    
    
    
    LOGIN_LINK = (By.CSS_SELECTOR, "#login_link")
    LOGIN_LINK_INVALID = (By.CSS_SELECTOR, "#login_link_inc")

    EMPTY_BASKET_TAG = (By.CSS_SELECTOR, "#content_inner > p")
    NOT_EMPTY_BASKET_TAG = (By.CSS_SELECTOR, ".basket-items")
    USER_ICON = (By.CSS_SELECTOR, ".icon-user")
    



