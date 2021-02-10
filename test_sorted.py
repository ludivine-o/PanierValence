class Objet:
    def __init__(self, value, name):
        self.value = value
        self.name = name



if __name__ == '__main__':
    obj_un = Objet(1, 'Pierre')
    obj_deux = Objet(2, 'Paul')

    liste_obj= []

    liste_obj.append(obj_deux)
    liste_obj.append(obj_un)

    for obj in liste_obj:
        print(obj.name)

    sorted_list = sorted(liste_obj, key=lambda objet : objet.value)

    for obj in sorted_list:
        print(obj.name)
