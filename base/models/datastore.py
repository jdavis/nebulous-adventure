import logging

from base import world

from google.appengine.ext import db
from google.appengine.api import memcache


def mem_get(key_property):
    def wrapper(f):
        def get(*args, **kwargs):
            model = memcache.get(args[0])
            if model is not None:
                return model

            model = f(*args, **kwargs)

            if hasattr(model, key_property):
                memcache.set(getattr(model, key_property),
                             model)

            return model
        return get
    return wrapper


def mem_put(key_property):
    def wrapper(f):
        def put(*args, **kwargs):
            model = args[0]
            if hasattr(model, key_property):
                memcache.set(getattr(model, key_property),
                             model)
            return f(*args, **kwargs)
        return put
    return wrapper


def mem_delete(key_property):
    def wrapper(f):
        def delete(*args, **kwargs):
            model = args[0]
            if hasattr(model, key_property):
                memcache.delete(getattr(model, key_property))
            return f(*args, **kwargs)
        return delete
    return wrapper


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

        area = Area.all().filter('name', name).filter('player', self.player).get()

        if area is None:
            data = world.get_area(room_name=name)

            if data is None:
                return None

            area = Area.new(self.player, data, temp_key=self.temp_key)

        return area

    def put_player(self, player):
        player.put()

    def delete_player(self, player):
        db.delete(player)

    def put_area(self, area):
        area.put()

    def get_player(self):
        from base.models import Player

        player = Player.all().filter('player_id', self.uid).get()
        self.player = player

        return player

    def create_player(self):
        from base.models import Player

        player = Player(player_id=self.uid)
        self.put_player(player)

        return player

datastore = DataStore()
