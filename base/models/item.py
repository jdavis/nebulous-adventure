from google.appengine.ext import db


class Item(db.Model):
    name = db.StringProperty()
    description = db.StringProperty()
    available = db.BooleanProperty(default=True)
    eat_reaction = db.StringProperty()
    use_reaction = db.StringProperty()

    # Relational Attributes
    owner = db.ReferenceProperty(collection_name='items')

    @classmethod
    def new(cls, data):
        item = cls(name=data['name'],
                   description=data['description'],
                   eat_reaction=data['eat_reaction'],
                   use_reaction=data['use_reaction'])
        item.put()

        return item
