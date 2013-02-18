from base import models


class Direction():
	North, South, East, West, Unknown = range(5)
	Direction_Dictionary = {'n':North, 'north':North,
							's':South, 'south':South,
							'e':East, 'east':East,
							'w':West, 'west':West}

	def translate_direction(self, direction):
		return self.Direction_Dictionary.get(direction.lower(), self.Unknown)

	def map_areas(self,n,s,e,w):
		return [n,s,e,w]

def generate_test_world():
	a = models.Area(name = 'start', description = 'start description')
	a.put()
	a.connecting_areas = map_areas(a.key(), a.key(), a.key(), a.key())
	a.put()

	p = models.Player(name='rob')
	p.put()

	w = models.World(area = a.key(), player = p.key(), x = 'no')
	w.put()


def look(world_key, direction):
	look_direction = Direction().translate_direction(direction)
	world = models.get_world_by_key(world_key)
	return world.area.get_direction_description(look_direction)

def move(world_key, direction):
	look_direction = Direction().translate_direction(direction)
	world = models.get_world_by_key(world_key)
	new_area = world.area.get_direction(look_direction)
	world.area = new_area
	world.put()
	return new_area.description


