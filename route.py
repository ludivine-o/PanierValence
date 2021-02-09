import requests
import json


def test():
    key = '1sAIpH7ZQ8EPzzLg8SeAfjtDsKAfhubd'
    origine = '3 Grande Rue, Valence, FR'
    dest = '10 rue Faventines, Valence, FR'

    json_data = {
    "locations": [
        "3 Grande Rue, Valence, FR",
        "10 rue Faventines, Valence, FR",
        "1 Avenue de Romans, Valence, FR"
    ],
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
    response = requests.post('http://www.mapquestapi.com/directions/v2/route?key='+key, json.dumps(json_data))
    print(response.json())
    json_name_route = 'result_route.json'
    with open(json_name_route, 'w') as json_result:
        json.dump(response.json(), json_result)



if __name__ == '__main__':
    test()
