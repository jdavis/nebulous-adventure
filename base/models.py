from google.appengine.ext import db


class Game(object):
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
    script = db.StringProperty()

    def talk(self):
        return script


class Player(db.Model):
    inventory = db.ListProperty(db.Key)
    current_area_key = db.StringProperty()

    def get_item(self, item_name):
        item = DataStore().get_item_by_name(item_name)
        if item is not None and item.key() in inventory:
            return item
        return None

    def get_direction(self, direction):
        return DataStore().get_area_by_id(current_area_key)

    def get_current_area(self):
        pass

    def set_area(self, area):
        pass

    def eat_item(self, item_name):
        pass


class Area(db.Model):
    description = db.StringProperty()

    def get_description(self):
        return description

    def get_direction(self, direction):
        pass

    def talk_to(self, char_name):
        character = DataStore().get_character_by_name(char_name)
        if character is not None:
            return character.talk()
        return 'Character DNE'

    def look(self, direction):
        pass


class Item(db.Model):
    name = db.StringProperty()
    description = db.StringProperty()

    def get_description(self):
        return description

    def eat_item(self):
        pass


class DataStore(object):
    def get_item_by_name(self, item_name):
        return Item.all().filter('name', item_name).get()

    def put_player(self, player):
        player.put()

    def get_player(self, id):
        return db.get(id)

    def get_character_by_name(self, name):
        return Character.all().filter('name', item_name).get()

    def get_area_by_id(self, id):
        return db.get(id)
