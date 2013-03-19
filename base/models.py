from google.appengine.ext import db


class Game(object):
    def look(self, uid, direction):
        player = DataStore().get_player(uid)
        area = player.get_direction(direction)
        if area is not None:
            return area.get_description()
        return 'Nothing over there...'

    def move(self, uid, direction):
        player = DataStore().get_player(uid)
        area = player.get_direction(direction)
        if area is not None:
            to_return = player.set_area(area)
            player.put()
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
        cur_area = self.get_current_area()
        if cur_area is not None:
            return cur_area.get_direction(direction)
        return None

    def get_current_area(self):
        return DataStore().get_area_by_id(current_area_key)

    def set_area(self, area):
        current_area_key = area.key()
        return area.get_description

    def eat_item(self, item_name):
        item = self.get_item(item_name)
        return item.eat()


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
        area = self.get_direction(direction)
        if area is not None:
            return area.get_description()
        return 'Area DNE'


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
