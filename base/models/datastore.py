from google.appengine.ext import db
import logging


class DataStore(object):
    def get_item_by_name(self, item_name):
        from base.models import Item
        return Item.all().filter('name', item_name).get()

    def get_character_by_name(self, name):
        from base.models import Character
        return Character.all().filter('name', name).get()

    def get_area_by_name(self, name):
        from base.models import Area
        return Area.all().filter('name', name).get()

    def put_player(self, player):
        player.put()

    def put_area(self,area):
        area.put()

    def get_player(self, uid):
        from base.models import Player
        player = Player.all().filter('player_id', uid).get()
        if player is None:
            player = Player(player_id = uid, inventory = [], current_area_name = 'start')
            self.put_player(player)
        return player