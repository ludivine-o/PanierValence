import os
import webbrowser
from pprint import pprint

import jinja2
import requests
import json
import math

import weasyprint


class Commerce:
    def __init__(self, nom, adr):
        self.nom = nom
        self.adr = adr
        self.y = 0
        self.x = 0
        self.distance = 0

    def get_nom(self):
        return self.nom

    def get_adr(self):
        return self.adr

    def get_dist(self):
        return self.distance

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_dist(self, dist):
        self.distance = dist

    def set_coord(self, x, y):
        self.x = x
        self.y = y

    def to_string(self):
        return "je suis "+self.nom+" et ma distance du dépot est de : "+str(round(self.distance))


# retourne une liste d'objet de type Commercant
def get_data_from_json_file():
    liste_commerces = []
    with open('result_location.json') as file:
        data = json.load(file)
        for list_data in data:
            commerce = Commerce(list_data[0], list_data[1])
            liste_commerces.append(commerce)
    return liste_commerces

# appel API pour retourner un JSON avec les coord
def get_route_informations(commerce_list):
    adress_data = []
    for commerce in commerce_list:
        adress_data.append(commerce.get_adr())
    key = '1sAIpH7ZQ8EPzzLg8SeAfjtDsKAfhubd'
    json_data = {
    "locations": adress_data,
    "options": {
        "avoids": [],
        "avoidTimedConditions": False,
        "doReverseGeocode": True,
        "shapeFormat": "raw",
        "generalize": 0,
        "routeType": "fastest",
        "timeType": 1,
        "locale": "en_US",
        "unit": "m",
        "enhancedNarrative": False,
        "drivingStyle": 2,
        "highwayEfficiency": 21.0
    }
}
    # response = requests.get('http://www.mapquestapi.com/directions/v2/route?key='+key+'&from=from='+origine+'&to='+dest+'&outFormat=json&ambiguities=ignore&routeType=fastest&doReverseGeocode=false&enhancedNarrative=false&avoidTimedConditions=false')
    response = requests.post('http://www.mapquestapi.com/directions/v2/optimizedroute?key='+key, json.dumps(json_data))
    json_name_route = 'result_route.json'
    with open(json_name_route, 'w') as json_result:
        json.dump(response.json(), json_result)

#utilise le JSOn de l'API pour ajouter les coord à la liste d'objet Commercant
def get_list_addresses_coord(liste_commercant):

    with open('result_route.json') as file:
        data = json.load(file)
        for (item, commercant) in zip(data['route']['locations'], liste_commercant):
            lng = item['displayLatLng']['lng']
            lat = item['displayLatLng']['lat']
            coord = lat, lng
            commercant.set_coord(lng, lat)
        return liste_commercant


def calcul_distance(origine, coord2):
    R = 6372800  # Earth radius in meters
    lat1, lon1 = origine
    lat2, lon2 = coord2
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def tri_par_distance(liste_obj_commercant_coord):
    origin_mairie_valence = 44.9331614, 4.892158
    for commerce in liste_obj_commercant_coord:
        coord = commerce.get_y(), commerce.get_x()
        dist = calcul_distance(origin_mairie_valence, coord)
        commerce.set_dist(dist)
    liste_obj_commercant_coord =  sorted(liste_obj_commercant_coord, key=lambda commerce : commerce.distance)
    return liste_obj_commercant_coord

def get_map_url(liste_obj_commercant_coord):
    compteur_q = 1
    url = 'http://www.mapquest.com/embed?'
    for commerce in liste_obj_commercant_coord:
        if compteur_q == 1:
            url += 'q1='
        else:
            to_add = '&q' + str(compteur_q) +'='
            url += to_add
        url += commerce.get_adr()
        compteur_q += 1
    url += '&maptype=map'
    # url = 'http://www.mapquest.com/embed?q1='+ adress1 +'&q2='+adress2+'&q3='+adress3+'&maptype=map'
    # url = http://www.mapquest.com/embed?q1=Place de la Concorde, paris, FR&q2=promenade des anglais, nice, FR&q3=Place Bellecour, Lyon, FR&maptype=map
    return url

def generate_txt(liste_comm_obj_coord, url):
    fichier = open("itineraire.txt", "w")
    str = set_txt(liste_comm_obj_coord)
    fichier.write("\nItineraire\n"+ str + "\nlien vers mapquest : \n" + url)
    fichier.close()

def set_txt(liste_comm_obj_coord):
    str = ""
    for comm in liste_comm_obj_coord:
        str += ("Commerce : "+comm.get_nom()+' , '+comm.get_adr()+", \n")
    return str

def generate_html(liste_comm_obj_coord, url):
    str = set_txt(liste_comm_obj_coord)
    table = ['tata', 'tutu', 'toto']
    text = '''
    <html>
        <header>
            <img src="data/logo.png">
        <body>
            <h1>Liste des commercants : </h1>
            <ul>
                <li>{}</li>
                <li>{}</li>
                <li>{}</li>
            </ul>
            <h3><a href="{}" target="_blank">Lien vers l'itineraire sur MapQuest</a></h3>
            
        </body>
    </html>
    '''.format(table[0], table[1], table[2], url)
    file = open("itineraire.html", "w")
    file.write(text)
    file.close()
    filename = 'file:///' + os.getcwd() + '/' + 'itineraire.html'
    webbrowser.open_new_tab(filename)


if __name__ == '__main__':
    origin_mairie_valence = 44.9331614,4.892158
    # liste_test = ['3 Grande Rue, Valence, FR', '10 rue Faventines, Valence, FR', '58 avenue Victor Hugo, Carpentras, FR']
    # get_route_informations(liste_test)
    # get_list_addresses_coord()
    # london_coord = 51.5073219, -0.1276474
    # cities = {
    #     'berlin': (52.5170365, 13.3888599),
    #     'vienna': (48.2083537, 16.3725042),
    #     'sydney': (-33.8548157, 151.2164539),
    #     'madrid': (40.4167047, -3.7035825)
    # }
    # for city, coord in cities.items():
    #     distance = calcul_distance(london_coord, coord)
    #     print(city, distance)

    list_obj_commercant = get_data_from_json_file()
    get_route_informations(list_obj_commercant)
    list_obj_commercant = get_list_addresses_coord(list_obj_commercant)
    list_obj_commercant = tri_par_distance(list_obj_commercant)
    print(get_map_url(list_obj_commercant))
    generate_txt(list_obj_commercant, get_map_url(list_obj_commercant))
    generate_html(list_obj_commercant, get_map_url(list_obj_commercant))


