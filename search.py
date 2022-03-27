import sys
from io import BytesIO
import requests
from PIL import Image
from yandex_map_helper import set_map_params


# python search.py Москва, ул. Ак. Королева, 12

toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

# Преобразуем ответ в json-объект
json_response = response.json()

# Получаем первый топоним из ответа геокодера.

toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
# Координаты центра топонима:
toponym_coodrinates = toponym["Point"]["pos"]
# Долгота и широта:
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
# Дельта
corners = toponym['boundedBy']['Envelope']
delta = str(float(corners['upperCorner'].split()[0]) - float(corners['lowerCorner'].split()[0]))
print(delta)

# Собираем параметры для запроса к StaticMapsAPI:

map_params = set_map_params(toponym_longitude, toponym_lattitude, delta)
map_params['pt'] = f"{toponym_longitude},{toponym_lattitude},pm2rdl"
print(map_params['pt'])
map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()
# Создадим картинку
# и тут же ее покажем встроенным просмотрщиком операционной системы
