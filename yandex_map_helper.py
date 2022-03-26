def set_map_params(toponym_longitude, toponym_lattitude, delta, l='map'):
    return {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join([delta, delta]),
    "l": l}
