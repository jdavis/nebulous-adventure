from base.game import Game


class GameController(object):

    def __init__(self, uid, game_key=None):
        self.uid = uid
        self.game_key = game_key

    def attack(self, name, item_name):
        return Game(self.uid).attack(name, item_name)

    def look(self, direction=""):
        return Game(self.uid).look(direction)

    def move(self, direction):
        return Game(self.uid).move(direction)

    def examine(self, item_name):
        return Game(self.uid).examine(item_name)

    def talk(self, char_name):
        return Game(self.uid).talk(char_name)

    def eat(self, item_name):
        return Game(self.uid).eat(item_name)

    def take(self, item_name):
        return Game(self.uid).take(item_name)

    def put(self, item_name):
        return Game(self.uid).put(item_name)

    def die(self):
        return Game(self.uid).die()

    def use(self, item_name):
        return Game(self.uid).use(item_name)

    def inventory(self):
        return Game(self.uid).inventory()

    def help(self, command=None):
        return Game(self.uid).help(command)

    def status(self):
        return Game(self.uid).status()

    def start(self, *args):
        return Game(self.uid).start(*args)
