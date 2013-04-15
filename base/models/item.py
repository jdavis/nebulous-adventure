from google.appengine.ext import db
import logging

class Item(db.Model):
    name = db.StringProperty()
    description = db.StringProperty()
    eat_reaction = db.StringProperty()
    use_reaction = db.StringProperty()

    def get_description(self):
        return self.description

    def eat(self):
        return self.eat_reaction

    def use(self):
        return self.use_reaction

    def get_name(self):
        return self.name