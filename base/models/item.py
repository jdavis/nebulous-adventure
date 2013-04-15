from google.appengine.ext import db
import logging

class Item(db.Model):
    name = db.StringProperty()
    description = db.StringProperty()

    def get_description(self):
        return self.description

    def eat_item(self):
        pass

    def get_name(self):
        return self.name