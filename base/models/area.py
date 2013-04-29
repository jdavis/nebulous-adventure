from base import world

from .datastore import datastore
from .player import Player

from google.appengine.ext import db


class Area(db.Model):
    name = db.StringProperty(required=True)
    description = db.StringProperty(required=True)
    temp_key = db.StringProperty()

    area_north = db.StringProperty()
    area_east = db.StringProperty()
    area_south = db.StringProperty()
    area_west = db.StringProperty()

    # Relational Properties
    player = db.ReferenceProperty(Player, collection_name='areas')

    @classmethod
    def new(cls, player, data):
        area = cls(name=data['name'],
                   description=data['description'],
                   area_north=data['connecting_areas']['n'],
                   area_east=data['connecting_areas']['e'],
                   area_south=data['connecting_areas']['s'],
                   area_west=data['connecting_areas']['w'],
                   player=player)

        area.put()

        for name in data['items']:
            item = datastore.get_item_by_name(name)
            item.owner = area
            item.put()

        return area

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_neighbor(self, d):
        if d == 'n' or d == 'north':
            name = self.area_north
        elif d == 'e' or d == 'east':
            name = self.area_east
        elif d == 's' or d == 'south':
            name = self.area_south
        elif d == 'w' or d == 'west':
            name = self.area_west
        else:
            return

        area = Area.all().filter('name', name).filter('player', self.player).get()

        if area is None:
            data = world.get_area(room_name=name)
            area = Area.new(self.player, data)
            area.put()

        return area

    def get_character(self, name):
        character = self.characters.filter('name', name).get()

        if character is None:
            character = datastore.get_character_by_name(self, name)

        return character

    def talk_to(self, name):
        character = self.get_character(name)

        if character is None:
            return 'There is no one named that here.'

        return character.script

    def attack(self, name, item):
        character = self.get_character(name)

        if character is None:
            return 'There is no one named that here.'

        return character.attack(item)

    def take_item(self, name):
        return self.items.filter('name', name).get()

    def add_item(self, item):
        if item is None:
            return

        item.owner = self
        item.put()
