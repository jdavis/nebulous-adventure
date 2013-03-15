from google.appengine.ext import db


class Game(Object):
    def look(self, uid, direction):
        pass

    def move(self, uid, direction):
        pass

    def examine(self, uid, item_name):
        pass

    def talk(self, uid, char_name):
        pass

    def eat(self, uid, item_name):
        pass


class Character(db.Model):
    def talk(self):
        pass


class Player(db.Model):
    def get_item(self, item_name):
        pass

    def get_direction(self, direction):
        pass

    def get_current_area(self):
        pass

    def set_area(self, area):
        pass

    def eat_item(self, item_name):
        pass


class Area(db.Model):
    def get_description(self):
        pass

    def get_direction(self, direction):
        pass

    def talk_to(self, char_name):
        pass

    def look(self, direction):
        pass


class Item(db.Model):
    def get_description(self):
        pass

    def eat_item(self):
        pass


class DataStore(Object):
    def get_item_by_name(self, item_name):
        pass

    def put_player(self, player):
        pass

    def get_player(self, id):
        pass

    def get_character_by_name(self, name):
        pass

    def get_area_by_id(self, id):
        pass