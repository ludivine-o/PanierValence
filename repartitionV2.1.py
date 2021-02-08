import json


# classe represetant un article du panier
class Article:

    def __init__(self, id, name, price, retailer):
        self.nom = name
        self.id = id
        self.price = price
        self.retailer = retailer

    def get_price(self):
        return self.price

    def get_name(self):
        return self.nom

    def get_id(self):
        return self.id

    def get_retailer(self):
        return self.retailer

    def to_string(self):
        string = 'Designation : ' + self.nom + ',  prix : ' + str(self.price)
        return string


# classe represetant un commercant dont au moins un article est dans le panier
class Retailer:

    def __init__(self, name, total):
        self.name = name
        self.total = total

    def get_total(self):
        return self.total

    def set_total(self, new_value):
        self.total = new_value

    def add_to_total(self, new_value):
        new_total = self.get_total() + new_value
        self.set_total(new_total)

    def to_string(self):
        string = 'Commercant : ' + self.name + ',  Total du : ' + str(self.total)
        return string

    def __eq__(self, other_retailer):
        return self.name == other_retailer.name


# Fonction qui récupere la liste des articles du panier issues du fichier json, et qui crée une liste d'objet "article"
def get_list_item_from_json(fileJson):
    item_list = []
    with open(fileJson) as file:
        data = json.load(file)
        for item in data['cart']['lineItems']:
            total_price = item['totalPrice']
            id_retailer = item['customTextFields']
            id_article = item['id']
            name_article = item['name']
            article = Article(id_article, name_article, total_price, id_retailer[0])
            item_list.append(article)
        return item_list

# Fonction qui récupere l'ID du cart traité
def get_id_cart_from_json(fileJson):
    item_list = []
    with open(fileJson) as file:
        data = json.load(file)
        cart_id = data['cart']['id']
        return cart_id

# Fonction qui crée une liste un commercant dont au moins un article est dans le panier
def get_repartition(items):
    results = []
    for article in items:
        retail = article.get_retailer()
        totalPrice = article.get_price()
        current_retailer = Retailer(retail, totalPrice)

        is_existant_in_list = False

        for existing_retailer in results:
            if current_retailer.__eq__(existing_retailer):
                is_existant_in_list = True
                existing_retailer.add_to_total(current_retailer.get_total())
        if not is_existant_in_list:
            results.append(current_retailer)
    return results


def get_json_file_repartition(list_repartition, cart_id):
    json_data = ''
    for object in list_repartition:
        json_str = json.dumps(object.__dict__)
        #print(json_str)
        json_data = json_data + json_str
        #print(json_data)
    json_name = 'result_repartition' + cart_id + '.json'
    with open(json_name, 'w') as json_result:
        json.dump(json_data, json_result)


def repartition(json_file_name):
    item_list = get_list_item_from_json(json_file_name)
    retailers_list = get_repartition(item_list)
    cart_id = get_id_cart_from_json(json_file_name)
    get_json_file_repartition(retailers_list, cart_id)

if __name__ == '__main__':
    repartition('cart3.json')








