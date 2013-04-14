from google.appengine.ext import db

import logging

class Player(db.Model):
    player_id = db.StringProperty()
    inventory = db.StringListProperty()
    current_area_name = db.StringProperty()

    def get_item(self, item_name):
        from base.models import DataStore
        if item_name in inventory:
            return DataStore().get_item_by_name(item_name)
        return None

    def add_item(self, item):
        if item is not None:
            self.inventory.append(item.get_name())
            return item.get_description()
        return "What item?"

    def get_current_area(self):
        from base.models import DataStore
        return DataStore().get_area_by_name(self.current_area_name)

    def set_area(self, area):
        self.current_area_name = area.get_name()
        return area.get_description()

    def eat_item(self, item_name):
        item = self.get_item(item_name)
        return item.eat()