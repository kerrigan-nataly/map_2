import sys
import requests
# python search.py Москва, ул. Ак. Королева, 12

# Первый запрос > узнали координаты
toponym_to_find = " ".join(sys.argv[1:])
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)
json_response = response.json()

toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"].split(" ")

# Второй запрос > узнали район
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": ",".join(toponym_coodrinates),
    "kind": "district",
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)
json_response = response.json()

GeocoderMetaData = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]
district = GeocoderMetaData["Address"]["Components"][-1]["name"]


print(district)
