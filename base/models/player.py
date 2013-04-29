import logging

from .datastore import datastore

from google.appengine.ext import db


class Player(db.Model):
    player_id = db.StringProperty(required=True)
    private_id = db.StringProperty()
    current_area = db.ReferenceProperty()

    def inventory(self):
        return self.items.filter('available', True)

    def get_item(self, item_name):
        for item in self.items.filter('available', True):
            if item.name == item_name:
                return item

        return None

    def add_item(self, item):
        if item is None:
            return

        item.owner = self
        item.put()

    def get_current_area(self):
        if self.current_area is None:
            area = datastore.get_area_by_name()
            self.set_current_area(area)

        return self.current_area

    def set_current_area(self, area):
        self.current_area = area
        self.put()

    def use_item(self, item_name):
        item = self.get_item(item_name)

        if item is None:
            return 'You don\'t have that item in your inventory.'

        return item.use_reaction

    def eat_item(self, item_name):
        item = self.get_item(item_name)

        if item is None:
            return 'You don\'t have that item in your inventory.'

        item.available = False
        item.put()

        return item.eat_reaction

    def take_item(self, item_name):
        item = self.get_item(item_name)
        item.delete()

        return item
