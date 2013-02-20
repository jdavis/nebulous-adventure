from base import models


class Direction():
	North, South, East, West, Unknown = range(5)
	Direction_Dictionary = {'n':North, 'north':North,
							's':South, 'south':South,
							'e':East, 'east':East,
							'w':West, 'west':West}

	def translate_direction(self, direction):
		return self.Direction_Dictionary.get(direction.lower(), self.Unknown)

	# helps keep consistancy with the mapping 
	# when generating areas 
	def map_areas(self,n,s,e,w):
		return [n,s,e,w]

class Game():

	# can be ran from interactive console to generete
	# a quick test world
	#
	# from base import utils
	# utils.Game().generate_test_world()
	def generate_test_world(self):
		a = models.Area(name = 'start', description = 'start description')
		a.put() # we need to put to generate key
		a.connecting_areas = Direction().map_areas(a.key(), a.key(), a.key(), a.key())
		a.put()

		p = models.Player(name='rob', area = a)
		p.put()

	def look(self, uid, args):
		# todo argument error checking
		look_direction = Direction().translate_direction(args[0])
		payer = models.Actions().get_player_by_key(uid)
		return payer.area.get_direction_description(look_direction)


	def move(self, uid, args):
		# todo argument error checking
		look_direction = Direction().translate_direction(args[0])
		player = models.Actions().get_player_by_key(uid)
		new_area = player.area.get_direction(look_direction)
		player.area = new_area
		player.put()
		return new_area.description

	command_dict = {'look':look,
					'move':move}


