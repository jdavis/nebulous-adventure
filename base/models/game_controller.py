from base.models import Game
import logging

class GameController(object):

    def look(self, uid, direction=""):
        return Game().look(uid,direction)

    def move(self, uid, direction):
        return Game().move(uid,direction)

    def examine(self, uid, item_name):
        return Game().examine(uid,item_name)

    def talk(self, uid, char_name):
        return Game().talk(uid,char_name)

    def eat(self, uid, item_name):
        return Game().eat(uid,item_name)

    def take(self, uid, item_name):
        return Game().take(uid,item_name)

    def die(self, uid):
        return Game().die(uid)

    def use(self, uid, item_name):
        return Game().use(uid, item_name)

    def inventory(self, uid):
        return Game().inventory(uid)

    def help(self, uid, command=None):
        return Game().help(uid,command)
