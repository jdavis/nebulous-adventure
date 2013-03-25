from google.appengine.ext import db
from base import utils
import logging


class Game(object):
    command_list = [
        'look',
        'move',
        'examine',
        'talk',
        'eat',
        'help',
    ]

    def look(self, uid, direction=""):
        """
        Look around at the room you are in.

        Usage:
            look [<direction>...]

        Options:
            north		Room to the north
            south		Room to the south
            east		Room to the east
            west		Room to the west

        EXAMPLE:
            look n s e
                Will print the descriptions of all the given rooms.

        NOTES:
            For convenience, the letters n, s, e, w can also be used.
        """

        player = DataStore().get_player(uid)
        cur_area = player.get_current_area()

        if cur_area is None:
            return 'It looks like there isn\'t any game data'

        if direction == "":
            return cur_area.get_description()

        area = utils.check_map(cur_area, direction)
        if area is not None:
            return area.get_description()
        return 'Nothing over there...'

    def move(self, uid, direction):
        """
        Move to a given location.

        Usage:
            move <direction>

        Options:
            north		Room to the north
            south		Room to the south
            east		Room to the east
            west		Room to the west

        EXAMPLE:
            move s
                Will move your current character to the room to the south (if
                able).

        NOTES:
            For convenience, the letters n, s, e, w can also be used.
        """

        player = DataStore().get_player(uid)
        area = utils.check_map(player.get_current_area(), direction)
        if area is not None:
            to_return = player.set_area(area)
            DataStore().put_player(player)
            return to_return
        return 'Ummmm I can not go over there...'

    def examine(self, uid, item_name):
        """
        Examine a given item(s) in your inventory or the room.

        Usage:
            examine [<item name>...]

        Options:
            Any valid item(s) name.

        EXAMPLE:
            examine sock
                Will print the description for the sock in the current room.
        """

        player = DataStore().get_player(uid)
        item = player.get_item(item_name)
        if item is not None:
            return item.get_description()
        return 'I do not have that item...'

    def talk(self, uid, char_name):
        """
        Talk to an NPC that is in your current area.

        Usage:
            talk <NPC name>

        Options:
            Any valid NPC name.

        EXAMPLE:
            talk uncle iroh
                Will print what Uncle Iroh has to say.
        """

        player = DataStore().get_player(uid)
        area = player.get_current_area()
        if area is not None:
            return area.talk_to(char_name)
        return 'There is no one by that name...'

    def eat(self, uid, item_name):
        """
        Eat the given item(s) that you requested.

        Usage:
            eat [<item name>...]

        Options:
            Any valid item name in the room or your inventory.

        EXAMPLE:
            eat cupcake
                Will consume the cupcake, mmmmmm.... cupcakes.
        """

        player = DataStore().get_player(uid)
        return player.eat_item(item_name)

    def help(self, uid, command=None):
        """
        Now you are just testing the limits of my knowlege.

        """

        if command is not None and command in Game.command_list:
            help_str = object.__getattribute__(self, command).__doc__
            return utils.trim_docstring(help_str)

        result = ['List of available commands:\n']

        if command is not None and command not in Game.command_list:
            return 'You expect me to know what that is?'

        for cmd in Game.command_list:
            if cmd == 'help':
                continue

            help_str = object.__getattribute__(self, cmd).__doc__

            # We only want the description
            line = '\t{command}\t{desc}'.format(command=cmd.lstrip(),
                                                desc=help_str.split('\n')[1])

            result.append(line)

        return '\n'.join(result)


class Character(db.Model):
    name = db.StringProperty()
    script = db.StringProperty()

    def talk(self):
        return self.script

    def get_name(self):
        return self.name


class Player(db.Model):
    player_id = db.StringProperty()
    inventory = db.StringListProperty()
    current_area_name = db.StringProperty()

    def get_item(self, item_name):
        if item_name in inventory:
            return DataStore().get_item_by_name(item_name)
        return None

    def get_current_area(self):
        return DataStore().get_area_by_name(self.current_area_name)

    def set_area(self, area):
        self.current_area_name = area.get_name()
        return area.get_description()

    def eat_item(self, item_name):
        item = self.get_item(item_name)
        return item.eat()


class Area(db.Model):
    description = db.StringProperty()
    name = db.StringProperty()
    characters = db.StringListProperty()

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def talk_to(self, char_name):
        if char_name in self.characters:
            character = DataStore().get_character_by_name(char_name)
            if character is not None:
                return character.talk()
        return 'Character DNE'


class Item(db.Model):
    name = db.StringProperty()
    description = db.StringProperty()

    def get_description(self):
        return description

    def eat_item(self):
        pass

    def get_name(self):
        return self.name


class DataStore(object):
    def get_item_by_name(self, item_name):
        return Item.all().filter('name', item_name).get()

    def get_character_by_name(self, name):
        return Character.all().filter('name', name).get()

    def get_area_by_name(self, name):
        return Area.all().filter('name', name).get()

    def put_player(self, player):
        player.put()

    def get_player(self, uid):
        player = Player.all().filter('player_id', uid).get()
        if player is None:
            player = Player(player_id = uid, inventory = [], current_area_name = 'start')
            self.put_player(player)
        return player
