from google.appengine.ext import db
import logging


class Area(db.Model):
    description = db.StringProperty()
    name = db.StringProperty()
    characters = db.StringListProperty()
    items = db.StringListProperty()

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def talk_to(self, char_name):
        from base.models import DataStore

        if char_name in self.characters:
            character = DataStore().get_character_by_name(char_name)
            if character is not None:
                return character.talk()
        return 'Character DNE'

    def take_item(self, item_name):
        from base.models import DataStore
        
        if item_name in self.items:
            item = DataStore().get_item_by_name(item_name)
            if item is not None:
                self.items.remove(item_name)
            return item
        return None
