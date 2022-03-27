import sys
import math
from io import BytesIO
import requests
from PIL import Image
from yandex_map_helper import set_map_params

def distance(coord1, coord2):
    cat1 = abs(float(coord1[0]) - float(coord2[0]))
    cat2 = abs(float(coord1[1]) - float(coord2[1]))
    dist = math.sqrt(cat1 ** 2 + cat2 ** 2)
    dist *= 111.1  # Перевод в километры
    return int(dist * 1000)


# python search.py Москва, ул. Ак. Королева, 12
# Адрес
toponym_to_find = " ".join(sys.argv[1:])
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)
json_response = response.json()

# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]

toponym_coodrinates = toponym["Point"]["pos"].split(" ")
toponym_longitude, toponym_lattitude = toponym_coodrinates

# Получаем аптеку
search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

address_ll = ','.join(toponym_coodrinates)
search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    'results': "1",
    "ll": address_ll,
    "type": "biz"}

apteka_response = requests.get(search_api_server, params=search_params)
apteka_json = apteka_response.json()

apteka = apteka_json["features"][0]
apteka_coodrinates = apteka["geometry"]["coordinates"]
apteka_longitude, apteka_lattitude = apteka_coodrinates
#print(apteka_json)

# Создание и вывод карты
map_params = {'l': 'map'}
map_params['pt'] = f"{toponym_longitude},{toponym_lattitude},pm2ntl~{apteka_longitude},{apteka_lattitude},pm2rdl"

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()
# ВЫвод информации об аптеке
# Рассчет расстояния
apteka_data = apteka["properties"]["CompanyMetaData"]
snippet = [apteka_data["address"],
           apteka_data["name"],
           apteka_data["Hours"]["text"],
           str(distance(apteka_coodrinates, toponym_coodrinates))]

print('\n'.join(snippet))

