from google.appengine.ext import db
from base import utils
import logging


class Game(object):
    def look(self, uid, direction=""):
        player = DataStore().get_player(uid)
        cur_area = player.get_current_area()

        if direction == "":
            return cur_area.get_description()

        area = utils.check_map(cur_area, direction)
        if area is not None:
            return area.get_description()
        return 'Nothing over there...'

    def move(self, uid, direction):
        player = DataStore().get_player(uid)
        area = utils.check_map(player.get_current_area(), direction)
        if area is not None:
            to_return = player.set_area(area)
            DataStore().put_player(player)
            return to_return
        return 'Ummmm I can not go over there...'

    def examine(self, uid, item_name):
        player = DataStore().get_player(uid)
        item = player.get_item(item_name)
        if item is not None:
            return item.get_description()
        return 'I do not have that item...'

    def talk(self, uid, char_name):
        player = DataStore().get_player(uid)
        area = player.get_current_area()
        if area is not None:
            return area.talk_to(char_name)
        return 'There is no one by that name...'

    def eat(self, uid, item_name):
        player = DataStore().get_player(uid)
        return player.eat_item(item_name)


class Character(db.Model):
    name = db.StringProperty()
    script = db.StringProperty()

    def talk(self):
        return self.script

    def get_name(self):
        return self.name


class Player(db.Model):
    player_id = db.StringProperty()
    inventory = db.StringListProperty()
    current_area_name = db.StringProperty()

    def get_item(self, item_name):
        if item_name in inventory:
            return DataStore().get_item_by_name(item_name)
        return None

    def get_current_area(self):
        return DataStore().get_area_by_name(self.current_area_name)

    def set_area(self, area):
        self.current_area_name = area.get_name()
        return area.get_description()

    def eat_item(self, item_name):
        item = self.get_item(item_name)
        return item.eat()


class Area(db.Model):
    description = db.StringProperty()
    name = db.StringProperty()
    characters = db.StringListProperty()

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def talk_to(self, char_name):
        if char_name in self.characters:
            character = DataStore().get_character_by_name(char_name)
            if character is not None:
                return character.talk()
        return 'Character DNE'


class Item(db.Model):
    name = db.StringProperty()
    description = db.StringProperty()

    def get_description(self):
        return description

    def eat_item(self):
        pass

    def get_name(self):
        return self.name


class DataStore(object):
    def get_item_by_name(self, item_name):
        return Item.all().filter('name', item_name).get()

    def get_character_by_name(self, name):
        return Character.all().filter('name', name).get()

    def get_area_by_name(self, name):
        return Area.all().filter('name', name).get()

    def put_player(self, player):
        player.put()

    def get_player(self, uid):
        player = Player.all().filter('player_id', uid).get()
        if player is None:
            player = Player(player_id = uid, inventory = [], current_area_name = 'start')
            self.put_player(player)
        return player