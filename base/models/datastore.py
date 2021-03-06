import logging

from base import world

from google.appengine.ext import db
from google.appengine.api import memcache


class DataStore(object):

    def __init__(self):
        self.uid = ''
        self.temp_key = None
        self.player = None

    def get_item_by_name(self, name):
        from base.models import Item

        data = world.get_item(name)

        if data is None:
            return None

        item = Item.new(data, temp_key=self.temp_key)

        return item

    def get_character_by_name(self, area, name):
        from base.models import Character

        data = world.get_character(name)

        if data is None:
            return None

        character = Character.new(area, data, temp_key=self.temp_key)

        return character

    def get_area_by_name(self, name=None):
        from base.models import Area

        area = Area.get(self.temp_key, name=name, player=self.player)

        if area is None:
            data = world.get_area(room_name=name)

            if data is None:
                return None

            area = Area.new(self.player, data, temp_key=self.temp_key)

        return area

    def save_game(self):
        from base import models

        for area in models.Area.all().filter('temp_key', self.temp_key).fetch(None):
            area.temp_key = None
            area.put()

        for item in models.Item.all().filter('temp_key', self.temp_key).fetch(None):
            item.temp_key = None
            item.put()

        for character in models.Character.all().filter('temp_key', self.temp_key).fetch(None):
            character.temp_key = None
            character.put()

    def put_player(self, player):
        player.put()

    def delete_player(self, player):
        db.delete(player)

    def put_area(self, area):
        area.put()

    def touch_player(self):
        logging.info('Touching player with %s', self.temp_key)
        player = self.get_player()

        if player is None:
            return None

        player.temp_key = self.temp_key
        player.put()
        return player

    def get_player(self):
        from base.models import Player

        player = Player.all().filter('player_id', self.uid).get()
        self.player = player

        return player

    def create_player(self):
        from base.models import Player
        return Player.new(self.uid, temp_key=self.temp_key)

datastore = DataStore()
