from repartitionV2 import Article, Retailer, get_list_item_from_json, \
    get_json_file_repartition, get_repartition, get_id_cart_from_json, send_data_location


def test_class_article():
    test_article = Article("id", "name", 12, "vendeur", "marignan 1515")
    assert test_article.get_id() == "id"
    assert test_article.get_name() == "name"
    assert test_article.get_price() == 12
    assert test_article.get_retailer_name() == "vendeur"
    assert test_article.get_retailer_loc() == "marignan 1515"
    assert test_article.to_string() == 'Designation : name,  prix : 12'


def test_class_retailer():
    test_retailer = Retailer("vendeur", 8, "marignan 1515")
    test_retailer2 = Retailer("other_vendor", 16, "12 rue du yahourt")
    assert test_retailer.name == "vendeur"
    assert test_retailer.total == 8
    new_value = 12
    assert test_retailer.get_loc() == "marignan 1515"
    assert test_retailer.get_total() == 8
    test_retailer.add_to_total(new_value)
    assert test_retailer.get_total() == 20
    test_retailer.set_total(8)
    assert test_retailer.get_total() == 8
    assert test_retailer.to_string() == 'Commercant : vendeur,  Total du : 8'
    assert test_retailer.__eq__(test_retailer2) == False
    assert test_retailer.__eq__(test_retailer)


def test_get_list_item_from_json():
    test_list = get_list_item_from_json('tests/test_cart.json')
    assert test_list[0].get_retailer_name() == "bob"
    assert test_list[0].get_retailer_loc() == "adresse de bob"
    assert test_list[0].get_price() == 20
    assert test_list[0].get_name() == "GogoGadget"
    assert test_list[0].get_id() == 1
    assert test_list[1].get_retailer_name() == "FOO"
    assert test_list[1].get_retailer_loc() == "adresse de FOO"
    assert test_list[1].get_price() == 100000
    assert test_list[1].get_name() == "GogoGadgetauPied"
    assert test_list[1].get_id() == 2
    assert test_list[2].get_retailer_name() == "bob"
    assert test_list[2].get_retailer_loc() == "adresse de bob"
    assert test_list[2].get_price() == 50
    assert test_list[2].get_name() == "GadgetAuBras"
    assert test_list[2].get_id() == 3
    assert test_list[3].get_retailer_name() == "FOO"
    assert test_list[3].get_retailer_loc() == "adresse de FOO"
    assert test_list[3].get_price() == 50
    assert test_list[3].get_name() == "GadgetAuPied"
    assert test_list[3].get_id() == 4
    assert len(test_list) == 4


def test_get_id_cart_from_json():
    test_cart_0 = get_id_cart_from_json('tests/test_cart.json')
    test_cart_1 = get_id_cart_from_json('data/cart1.json')
    test_cart_2 = get_id_cart_from_json('data/cart2.json')
    test_cart_3 = get_id_cart_from_json('data/cart3.json')
    test_simple = get_id_cart_from_json('tests/test_simple_reading.json')
    assert test_cart_0 == "6000dbd9-cb49-4066-820e-2d95cb1cart0"
    assert test_cart_1 == "6000dbd9-cb49-4066-820e-2d95cb1cart1"
    assert test_cart_2 == "6000dbd9-cb49-4066-820e-2d95cb1cart2"
    assert test_cart_3 == "6000dbd9-cb49-4066-820e-2d95cb1cart3"
    assert test_simple == "ID order"


def test_get_repartition():
    res_test_simple = get_repartition(get_list_item_from_json('tests/test_simple_reading.json'))
    assert len(res_test_simple) == 3
    assert res_test_simple[0].get_total() == 150
    assert res_test_simple[0].get_name() == "bob"
    assert res_test_simple[0].get_loc() == "adresse de bob"
    assert res_test_simple[1].get_total() == 130
    assert res_test_simple[1].get_name() == "tonton"
    assert res_test_simple[1].get_loc() == "adresse de tonton"
    assert res_test_simple[2].get_total() == 270
    assert res_test_simple[2].get_name() == "philiiiiippe !"
    assert res_test_simple[2].get_loc() == "adresse de philiiiiippe !"


def test_get_json_file_repartition():
    json = get_json_file_repartition(get_repartition(get_list_item_from_json('tests/test_simple_reading.json')), get_id_cart_from_json('tests/test_simple_reading.json'))
    assert json == "{\"name\": \"bob\", \"total\": 150, \"location\": \"adresse de bob\"}{\"name\": \"tonton\", \"total\": 130, \"location\": \"adresse de tonton\"}{\"name\": \"philiiiiippe !\", \"total\": 270, \"location\": \"adresse de philiiiiippe !\"}"


def test_send_data_location():
    data = send_data_location(get_repartition(get_list_item_from_json('tests/test_simple_reading.json')), get_id_cart_from_json('tests/test_simple_reading.json'))
    assert data == [['bob', 'adresse de bob'], ['tonton', 'adresse de tonton'], ['philiiiiippe !', 'adresse de philiiiiippe !']]

