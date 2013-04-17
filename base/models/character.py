from google.appengine.ext import db


class Character(db.Model):
    name = db.StringProperty()
    script = db.StringProperty()

    def talk(self):
        return self.script

    def get_name(self):
        return self.name
