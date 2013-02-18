from google.appengine.ext import db
# from base import actions

import logging


class Player(db.Model):
	name = db.StringProperty()
	items = db.ListProperty(db.Key)

class Area(db.Model):
	name = db.StringProperty() 	
	description = db.StringProperty()
	items = db.ListProperty(db.Key) 
	characters = db.ListProperty(db.Key)
	connecting_areas = db.ListProperty(db.Key) 

	def get_direction_description(self, direction):
		connecting_area = self.get_direction(direction)
		if connecting_area is not None:
			return connecting_area.description
		return 'Nothing over there'

	def get_direction(self, direction):
		new_area_key = self.connecting_areas[direction]
		return get_area_by_key(new_area_key)

class Character(db.Model):
	name = db.StringProperty() 	
	description = db.StringProperty()
	items = db.ListProperty(db.Key) 	
	script = db.StringProperty()

class Item(db.Model):
	name = db.StringProperty() 
	description = db.StringProperty()

class World(db.Model):
	player = db.ReferenceProperty(Player)
	area = db.ReferenceProperty(Area)


class SaveState(db.Model):
	world = db.ReferenceProperty()




def create_new_world():
	new_world = models.World()
	new_world.put()
	return new_world.key()

def get_world_by_key(key):
	return db.get(key)

def get_area_by_key(key):
	return db.get(key)	


