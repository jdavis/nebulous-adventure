from google.appengine.ext import db


import logging

class Item(db.Model):
	name = db.StringProperty() 
	description = db.StringProperty()

class Character(db.Model):
	name = db.StringProperty() 	
	description = db.StringProperty()
	items = db.ListProperty(db.Key) 
	script = db.StringProperty()

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
		return Actions().get_area_by_key(new_area_key)

class Player(db.Model):
	name = db.StringProperty()
	items = db.ListProperty(db.Key)
	area = db.ReferenceProperty(Area)

# Datatable actions
class Actions():
	def create_new_player(self):
		new_player = models.Player()
		new_player.put()
		return new_player

	def get_player_by_key(self, key):
		return db.get(key)

	def get_area_by_key(self, key):
		return db.get(key)	



