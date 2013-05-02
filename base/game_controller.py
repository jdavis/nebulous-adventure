from base.game import Game


class GameController(object):

    def __init__(self, uid, temp_key=None):
        self.uid = uid
        self.temp_key = temp_key

    def attack(self, name, item_name):
        return Game(self.uid, self.temp_key).attack(name, item_name)

    def look(self, direction=""):
        return Game(self.uid, self.temp_key).look(direction)

    def move(self, direction):
        return Game(self.uid, self.temp_key).move(direction)

    def examine(self, item_name):
        return Game(self.uid, self.temp_key).examine(item_name)

    def talk(self, char_name):
        return Game(self.uid, self.temp_key).talk(char_name)

    def eat(self, item_name):
        return Game(self.uid, self.temp_key).eat(item_name)

    def take(self, item_name):
        return Game(self.uid, self.temp_key).take(item_name)

    def put(self, item_name):
        return Game(self.uid, self.temp_key).put(item_name)

    def die(self):
        return Game(self.uid, self.temp_key).die()

    def use(self, item_name):
        return Game(self.uid, self.temp_key).use(item_name)

    def inventory(self):
        return Game(self.uid, self.temp_key).inventory()

    def help(self, command=None):
        return Game(self.uid, self.temp_key).help(command)

    def welcome(self):
        return Game(self.uid, self.temp_key).welcome()

    def start(self, *args):
        return Game(self.uid, self.temp_key).start(*args)

    def save(self, *args):
        return Game(self.uid, self.temp_key).save(*args)

    def color(self, *args):
        return Game(self.uid, self.temp_key).color(*args)
