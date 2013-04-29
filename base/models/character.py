from google.appengine.ext import db

from .area import Area


class Character(db.Model):
    name = db.StringProperty()
    script = db.StringProperty()
    temp_key = db.StringProperty()

    # Relational Properties
    area = db.ReferenceProperty(Area, collection_name='characters')

    @classmethod
    def new(cls, area, data, temp_key=None):
        character = cls(name=data['name'],
                        temp_key=temp_key,
                        script=data['script'],
                        area=area)
        character.put()

        return character

    def attack(self, item):
        #TODO: Make attack do something
        return '{0} says: Ouch!'.format(self.name.capitalize())

    def get_name(self):
        return self.name
