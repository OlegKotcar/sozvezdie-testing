#from bs4 import BeautifulSoup
import json
import urllib.request, requests, time
from datetime import datetime



producturl = "http://185.10.185.115:7777/tour/"
productAPIURL = "http://185.10.185.115:7777/api/tour/"
orderURL = "http://185.10.185.115:7777/api/Order"

#PARAMS = {'status':404} 
#r = requests.get(url = "http://185.10.185.115:7777/api/tour/0", params = PARAMS) 
#data = r.json() 



payload = {
  "items": [
    {
      "tourId": 0,
      "start": "2020-11-03T02:42:47.419Z",
      "price": 0
    }
  ],
  "total": 0,
  "registration": {
    "name": "string",
    "email": "string",
    "password": "string",
    "cardNumber": "string",
    "cardName": "string",
    "cardExpiry": "string",
    "cardCvc": "string"
  }
}

payloadError = {
  "items": [
    {
      "tourId": 0,
      "start": "2020-11-03T02:42:47.419Z",
      "price": 0
    }
  ],
  "total": 0,
  "registration": {
    "name": "string",

  }
}


payloadOK = {"items": [{"tourId": 0, "start": "2020-11-03T02:42:47.419Z", "price": 0}], "total": 0, "registration": {"name": "User Name", "email": "111@111.com", "password": "1qaz2wsx", "cardNumber": "1111222233334444", "cardName": "User Name","cardExpiry": "10/22","cardCvc": "111"}}

payloadErrorExpDate = {"items": [{"tourId": 0, "start": "2020-11-03T02:42:47.419Z", "price": 0}], "total": 0, "registration": {"name": "User Name", "email": "111@111.com", "password": "1qaz2wsx", "cardNumber": "1111222233334444", "cardName": "User Name","cardExpiry": "10/12","cardCvc": "111"}}


# Пробуем покупку - проходят любые значения, главное совпадение данных
r = requests.post(orderURL, json = payloadOK)
print(f"Пробуем купить  - ответ сервера {r.status_code}")







with urllib.request.urlopen(productAPIURL) as url:
    data = json.loads(url.read().decode())
#    print(data)

descriptons = []

def find_duplicates(lst, item):
    return [key for key, x in enumerate(lst) if x == item]

def string_to_date(rawString):  
    return (datetime.strptime(rawString, "%Y-%m-%dT%H:%M:%S%z"))

# Проверяем доступность API туров по id
print('Проверяем доступность API туров по id')
for key in range (len(data)):
    r = requests.head(f"{productAPIURL}{key}")
    if r.status_code != 200:
        print(f"{productAPIURL}{key}  - Страница недоступна")
        continue
    else:  
    # если url существует, пробуем его открыть
        r = requests.get(f"{productAPIURL}{key}")
        #data = r.json() 
        if r.status_code != 200:
            print(f"Страница {productAPIURL}{key} имеет статус ошибки {r.status_code}, но в каталоге присутствует")
            continue
        else:
            print(f"API {productAPIURL}{key} отдает JSON")        
            pass
            
            


# Проверяем полное совпадение текста в разных продуктах
for key in range (len(data)):
    descriptons.append(data[key]["description"])
for key in range(len(descriptons)):
    doublelist = (find_duplicates(descriptons, descriptons[key]))
    if key in doublelist: # убираем ссылку на самого себя
        doublelist.remove(key)
    print (f"Описание для тура {producturl}{key} полностью повторяется в турах с id={doublelist}")
# id потом можно привязать к конечным url



# Проверим даты
for key in range (len(data)):
    nearStart = data[key]["periodStart"] # Ближайшая дата начала в каталоге
    nearEnd =  data[key]["periodEnd"]  # Ближайшая дата окончания в каталоге
    minPrice = data[key]["minPrice"]  # Минимальная цена в каталоге
    if nearStart == None:
        print(f"Для продукта {producturl}{key} нет ближайшей даты начала в каталоге")
    elif nearEnd == None:    
        print(f"Для продукта {producturl}{key} нет ближайшей даты окончания в каталоге")
    elif minPrice == None:
        print(f"Для продукта {producturl}{key} минимлаьной цены в каталоге")
    else:
    # Если даты есть, работаем с ними  Тут еще UTC надо учитывать
        dateNow = datetime.now()
        nearStart = string_to_date(nearStart)
        nearEnd =  string_to_date(nearEnd)          
        if nearStart > nearEnd:
            print(f"Для продукта {producturl}{key} в каталоге ближайшее начало тура {nearStart.date()} позже его окончания {nearEnd.date()}")
        else:
            print(f"Для продукта {producturl}{key} с датами начала и конца тура все ОК")          
        if nearStart.date() > dateNow.date():
            print(f"Для продукта {producturl}{key} в каталоге ближайшее начало тура {nearStart.date()} уже прошло, сегодня {dateNow.date()}")        
# Собираем массив дат с карточки чтобы проверить даты на самих карточках и срачвнить их с каталожными
    
    startDates = []
    endDates = []
    productPrices = []
    
    prices = (data[key]["prices"])
    if prices == None:
         print(f"Для продукта {producturl}{key} нет предложений по датам и ценам в каталоге")
    else:
        for price in prices:
            startDateInProduct = string_to_date(price.get("start"))
            endDateInProduct = string_to_date(price.get("end"))
            priceInProduct = price.get("priceValue")
            #print(f"{startDateInProduct.date()} ---- {endDateInProduct.date()}")
            if startDateInProduct > endDateInProduct:
                print(f"На карточке продукта {producturl}{key} ближайшее начало тура {startDateInProduct.date()} позже его окончания {startDateInProduct.date()}") 
            if startDateInProduct.date() > dateNow.date():
                print(f"На карточке продукта {producturl}{key} ближайшее начало тура {startDateInProduct.date()} позже его окончания {startDateInProduct.date()}")            
            if priceInProduct <= 0 or priceInProduct == None:
                print(f"На карточке продукта {producturl}{key} не указана или неверно указана стоимость {priceInProduct}")               
            startDates.append(startDateInProduct.date())
            endDates.append(endDateInProduct.date())
            productPrices.append(priceInProduct)
        #print(f"{startDates}")
        # Тут проверям ближайшие даты в каталоге и в карточке
        #print(min(startDates))
        if  nearStart.date() != (min(startDates)):
            print(f"Для продукта {producturl}{key} ближайшая дата в каталоге {nearStart.date()} отличается от ближайшей даты на карточке продукта {min(startDates)}")
        else:
            print(f"С ближайшими датами на карточке продукта {producturl}{key} все ОК")
        if minPrice != min(productPrices):
            print(f"Для продукта {producturl}{key} мин. цена в каталоге {minPrice} отличается от мин. цены на карточке продукта {min(productPrices)}")        
        else:
            print(f"Мин. цена в каталоге и на карточке продукта {producturl}{key} все ОК")
    
    
#---------------------------------------------------------------------------------------

print("--------------------Проверяем превью и фото продуктов----------------------------")

# Проверяем  заргузку thumb и картинок с карточек продуктов
for key in range (len(data)):
    print(f"---------------------------------Идет проверка photoCard {key}")
    if data[key]["photoCard"] == None:
        print(f"В продукте {producturl}{key} отсутствует превью и картинка продукта")
    else: 
        thumburl = (data[key]["photoCard"]).get('thumbnail')
        photourl = (data[key]["photoCard"]).get('photo')
        # проверяем доступность url для превью продукта
        if thumburl == "": 
            print(f"В продукте {producturl}{key} отсутствует ссылка на превью")
        else:
            r = requests.get(thumburl)
            if r.status_code != 200:
                print(f"На странице продукта {producturl}{key} неверная ссылка на превью, {thumburl} ")

    # проверяем доступность url для фото продукта
        if photourl == "": 
            print(f"в продукте {producturl}{key} отсутствует ссылка на фото")
        else:
            r = requests.get(photourl)
            if r.status_code != 200:
                print(f"На странице продукта {producturl}{key} неверная ссылка на фото, {photourl} ")              

    # -----------проверяем досутупность url и превью для фотоальбома -------
    print(f"---------------------------------Идет проверка photoAlbum {key}")
    
    photoalbum = data[key]["photoAlbum"]
    if data[key]["photoAlbum"] == None:
        print(f"В продукте {producturl}{key} отсутствует фотоальбом")
    else: 
        for i in range(len(photoalbum)): # цикл по всем картинкам в фотоальбоме
            thumburl = (photoalbum[i]).get('thumbnail')
            photourl = (photoalbum[i]).get('photo')
            #print(f"Это фоточка с альбома {photourl}")
            
            # проверяем доступность url для превью в фотоальбоме продукта
            if thumburl == "":
                print(f"В продукте {producturl}{key}, в фотоальбоме отсутствует ссылка на превью")
            else:
                r = requests.get(thumburl)
                if r.status_code != 200:
                    print(f"В фотоальбоме продукта {producturl}{key} неверная ссылка на превью, {thumburl} ")

            # проверяем доступность url для фото в фотоальбоме продукта
            if photourl == "":
                print(f"В продукте {producturl}{key}, в фотоальбоме отсутствует ссылка на фото")
            else:
                r = requests.get(photourl)
                if r.status_code != 200:
                    print(f"В фотоальбоме продукта {producturl}{key} неверная ссылка на фото, {photourl} ")


"""
{
description:	
Детальная информация по предложению

id*	integer($int64)
Идентификатор

title	string
Название

header	string
Заголовок

description	string
Описание

route	[...]
periodStart*	string($date-time)
Начало ближайшего периода

periodEnd*	string($date-time)
Окончание ближайшего периода

minPrice*	number($double)
Минимальная цена

photoCard	PhotoCard{...}
photoAlbum	[...]
prices	[...]
}

--------------------------------------------------
Заказ

{
  "items": [
    {
      "tourId": 0,
      "start": "2020-11-03T02:42:47.419Z",
      "price": 0
    }
  ],
  "total": 0,
  "registration": {
    "name": "string",
    "email": "string",
    "password": "string",
    "cardNumber": "string",
    "cardName": "string",
    "cardExpiry": "string",
    "cardCvc": "string"
  }
}

"""


