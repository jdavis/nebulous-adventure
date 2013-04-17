from google.appengine.ext import db


class Character(db.Model):
    name = db.StringProperty()
    script = db.StringProperty()

    def attack(self, item):
        #TODO: Make attack do something
        return '{0} says: Ouch!'.format(self.name.capitalize())

    def talk(self):
        return self.script

    def get_name(self):
        return self.name
