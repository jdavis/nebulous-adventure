import logging

from base import utils
from base.models import datastore


class Game(object):
    command_list = [
        'die',
        'eat',
        'examine',
        'help',
        'inventory',
        'look',
        'move',
        'take',
        'talk',
        'use',
        'put',
        'attack',
    ]

    def __init__(self, uid):
        datastore.uid = uid

    def look(self, direction=""):
        """
        Look around at the room you are in.

        Usage:
            look <direction>

        Options:
            north       Room to the north
            south       Room to the south
            east        Room to the east
            west        Room to the west

        EXAMPLE:
            look n s e w
                Will print the descriptions of all the given rooms.

        NOTES:
            For convenience, the letters n, s, e, w can also be used.
        """

        directions = [
            'n', 'north',
            'e', 'east',
            's', 'south',
            'w', 'west'
        ]

        player = datastore.get_player()
        current_area = player.get_current_area()

        if direction == "":
            return current_area.description

        if direction not in directions:
            return 'Invalid direction'

        neighbor = current_area.get_neighbor(direction)

        if neighbor is None:
            return 'There\'s nothing over there!'

        return neighbor.description

    def move(self, direction):
        """
        Move to a given location.

        Usage:
            move <direction>

        Options:
            north       Room to the north
            south       Room to the south
            east        Room to the east
            west        Room to the west

        EXAMPLE:
            move s
                Will move your current character to the room to the south (if
                able).

        NOTES:
            For convenience, the letters n, s, e, w can also be used.
        """

        player = datastore.get_player()
        current_area = player.get_current_area()

        next_area = current_area.get_neighbor(direction)

        if next_area is None:
            return 'Ummmm I can not go over there...'

        player.set_current_area(next_area)

        return next_area.description

    def examine(self, item_name):
        """
        Examine a given item in your inventory or the room.

        Usage:
            examine <item name>

        Options:
            Any valid item(s) name.

        EXAMPLE:
            examine sock
                Will print the description for the sock in the current room.
        """

        player = datastore.get_player()
        item = player.get_item(item_name)

        if item is None:
            return 'I do not have that item...'

        return item.description

    def talk(self, char_name):
        """
        Talk to an NPC that is in your current area.

        Usage:
            talk <NPC name>

        Options:
            Any valid NPC name.

        EXAMPLE:
            talk 'uncle iroh'
                Will print what Uncle Iroh has to say.
        """

        player = datastore.get_player()
        current_area = player.get_current_area()

        if current_area is None:
            return 'There is no one by that name...'

        return current_area.talk_to(char_name)

    def eat(self, item_name):
        """
        Eat the given item that you requested.

        Usage:
            eat <item name>

        Options:
            Any valid item name in the room or your inventory.

        EXAMPLE:
            eat cupcake
                Will consume the cupcake, mmmmmm.... cupcakes.
        """

        player = datastore.get_player()

        reaction = player.eat_item(item_name)
        datastore.put_player(player)

        return reaction

    def take(self, item_name):
        """
        Take the given item that you requested.

        Usage:
            take <item name>

        Options:
            Any valid item name in the surrounding area

        EXAMPLE:
            take sock
                Will add sock to your inventory.
        """
        player = datastore.get_player()
        current_area = player.get_current_area()

        item = current_area.take_item(item_name)

        if item is None:
            return 'That item doesn\'t exist here.'

        player.add_item(item)

        datastore.put_player(player)

        return item.description

    def put(self, item_name):
        """
        Put the given item down in the current area.

        Usage:
            put <item name>

        Options:
            Any valid item name in your inventory.

        EXAMPLE:
            put kitten
                You put the kitten down.
        """

        player = datastore.get_player()
        current_area = player.get_current_area()

        item = player.take_item(item_name)

        if item is None:
            return 'That item doesn\'t exist.'

        current_area.add_item(item)

        return 'You place the {0} in the {1}.'.format(item.name, current_area.name)

    def use(self, item_name):
        """
        Use the given item that you requested.

        Usage:
            use <item name>

        Options:
            Any valid item name in your inventory.

        EXAMPLE:
            use jetpack
                You are now floating in the air.
        """

        player = datastore.get_player()
        return player.use_item(item_name)

    def inventory(self):
        """
        Look into your inventory.

        Usage:
            look

        Options:
            None

        EXAMPLE:
            inventory
                Sock
                Sword
                Trombone
        """

        player = datastore.get_player()
        inventory = player.inventory()

        if inventory.count() == 0:
            return 'Your inventory is empty.'

        return '\n'.join(item.name.capitalize() for item in inventory)

    def attack(self, character_name, item_name):
        """
        Attack the given character with the given item

        Usage:
            use <character name> <item name>

        Options:
            Any valid character in the area.
            Any valid item name in your inventory.

        EXAMPLE:
            attack gollum
                Gollum: My preciouss...
        """

        player = datastore.get_player()
        item = player.get_item(item_name)
        current_area = player.get_current_area()

        if item is None:
            return 'You don\'t have that item.'

        return current_area.attack(character_name, item)

    def die(self):
        """
        Mysteriously become lifeless....

        Usage:
            die

        Options:
            None

        EXAMPLE:
            die
                You are now dead...
        """

        player = datastore.get_player()
        datastore.delete_player(player)

        return 'You are now dead...'

    def help(self, command=None):
        """
        Show the help for a given command.

        Usage:
            help <command>

        Options:
            A valid game command.

        EXAMPLE:
            help help
                [Prints this message]
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
            line = '\t{command}{desc}'.format(command=cmd.lstrip().ljust(10),
                                              desc=help_str.split('\n')[1])

            result.append(line)

        return '\n'.join(result)
