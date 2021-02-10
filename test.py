import webbrowser

from jinja2 import Environment, FileSystemLoader

class Objet:
    def __init__(self, value, name):
        self.value = value
        self.name = name


persons = [
    {'name': 'Andrej', 'age': 34},
    {'name': 'Mark', 'age': 17},
    {'name': 'Thomas', 'age': 44},
    {'name': 'Lucy', 'age': 14},
    {'name': 'Robert', 'age': 23},
    {'name': 'Dragomir', 'age': 54},
]


if __name__ == '__main__':
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.rstrip_blocks = True

    template = env.get_template('result.template.html')

    output = template.render(persons=persons)
    file = open("test.html", "w")
    file.write(output)
    file.close()
    #print(output)
    webbrowser.open_new_tab("test.html")
