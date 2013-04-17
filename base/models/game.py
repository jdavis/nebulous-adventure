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
        'take',
        'use',
        'inventory',
        'die',
    ]

    def look(self, uid, direction=""):
        """
        Look around at the room you are in.

        Usage:
            look [<direction>...]

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
        from base.models import DataStore
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
        from base.models import DataStore
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
        from base.models import DataStore
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
        from base.models import DataStore
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
        from base.models import DataStore
        player = DataStore().get_player(uid)
        reaction = player.eat_item(item_name)
        DataStore().put_player(player)
        return reaction

    def take(self, uid, item_name):
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
        from base.models import DataStore
        player = DataStore().get_player(uid)
        cur_area = player.get_current_area()
        item = cur_area.take_item(item_name)
        to_return = player.add_item(item)

        DataStore().put_player(player)
        DataStore().put_area(cur_area)

        return to_return

    def use(self, uid, item_name):
        """
        Use the given item(s) that you requested.

        Usage:
            use [<item name>...]

        Options:
            Any valid item name in your inventory.

        EXAMPLE:
            use jetpack
                You are now floating in the air.
        """
        from base.models import DataStore
        player = DataStore().get_player(uid)
        return player.use_item(item_name)


    def inventory(self, uid):
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
        from base.models import DataStore
        player = DataStore().get_player(uid)
        inventory = player.get_inventory()
        if len(inventory):
            return '\n'.join(inventory)
        return 'Your inventory is empty...'


    def die(self, uid):
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
        from base.models import DataStore
        player = DataStore().get_player(uid)
        DataStore().delete_player(player)
        return 'You are now dead...'


    def help(self, uid, command=None):
        """
        Now you are just testing the limits of my knowlege.

        """
        from base.models import DataStore
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