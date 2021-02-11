from route import Commerce, get_map_url, generate_html_v2, get_list_addresses_coord, get_route, get_data_from_json_file,\
    get_route_informations, set_txt, generate_txt


def test_class_Commerce():
    test_commerce = Commerce('Bob', '1 Place des Clercs, 26000 Valence, FR')
    assert test_commerce.get_nom() == 'Bob'
    assert test_commerce.get_adr() == '1 Place des Clercs, 26000 Valence, FR'
    test_commerce.set_dist(1234)
    assert test_commerce.get_dist() == 1234

def test_get_data_from_json_file():
    test_liste = get_data_from_json_file()
    assert test_liste[0].get_nom() == 'bob'
    assert test_liste[0].get_adr() == 'adresse de bob'
    assert len(test_liste) == 3

def test_get_map_url():
    json = get_route_informations(get_data_from_json_file())
    assert str(json) == '<Response [200]>'



