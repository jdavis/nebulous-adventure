from google.appengine.ext import db
from google.appengine.api import memcache

import logging

def mem_get(key_property):
    def wrapper(f):
        def get(*args, **kwargs):
            model = memcache.get(args[1])
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
            model = args[1]
            if hasattr(model, key_property):
                memcache.set(getattr(model, key_property), 
                             model)
            return f(*args, **kwargs)
        return put
    return wrapper

def mem_delete(key_property):
    def wrapper(f):
        def delete(*args, **kwargs):
            model = args[1]
            if hasattr(model, key_property):
                memcache.delete(getattr(model, key_property))
            return f(*args, **kwargs)
        return delete
    return wrapper

class DataStore(object):

    @mem_get('name')
    def get_item_by_name(self, item_name):
        from base.models import Item
        return Item.all().filter('name', item_name).get()

    @mem_get('name')
    def get_character_by_name(self, name):
        from base.models import Character
        return Character.all().filter('name', name).get()

    @mem_get('name')
    def get_area_by_name(self, name):
        from base.models import Area
        return Area.all().filter('name', name).get()

    @mem_put('player_id')
    def put_player(self, player):
        player.put()

    @mem_delete('player_id')
    def delete_player(self, player):
        db.delete(player)

    @mem_put('name')
    def put_area(self, area):
        area.put()

    @mem_get('player_id')
    def get_player(self, uid):
        from base.models import Player

        player = Player.all().filter('player_id', uid).get()
        if player is None:
            player = Player(player_id=uid, inventory=[], current_area_name='start')
            self.put_player(player)

        return player
