
# Source Code for Nebulous Adventure


## main.py

```python
#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os

from flask import Flask

from google.appengine.ext.webapp.util import run_wsgi_app

from base import urls as base_urls

app = Flask(__name__)

#
# Settings
#

# TODO: Make static for deployment
SECRET_KEY = 'this_is_our_secret_key'

#
# App Settings
#

base_urls.apply_urls(app)
app.secret_key = SECRET_KEY

if __name__ == '__main__':
    run_wsgi_app(app)

```

## base/__init__.py

```python

```

## base/game.py

```python
import logging
import os

from base import utils
from base import style
from base.models import datastore


class Game(object):
    command_list = [
        'attack',
        'color',
        'die',
        'eat',
        'examine',
        'font',
        'help',
        'inventory',
        'look',
        'move',
        'put',
        'resume',
        'save',
        'take',
        'talk',
        'use',
    ]

    def __init__(self, uid, temp_key=None):
        self.uid = uid
        self.temp_key = temp_key
        logging.info('Initing with temp_key = %s', temp_key)
        datastore.uid = uid
        datastore.temp_key = temp_key

    def welcome(self):
        if self.temp_key is not None:
            return 'I\'m sorry, Dave. I\'m afraid I can\'t do that.'

        new = """
        Welcome to The Nebulous Adventure.

        You look confused. Don't worry, everyone in The Nebulous Adventure is confused.

        If this is your first time playing, check out the `help` command.

        Once you have a feel for the game, go ahead and start a new game with the `start` command.

        If you are a returning player, run the `resume` command with your given password. Or go to the URL that you were supplied.

        """

        returning = """
        Welcome back to The Nebulous Adventure.

        It looks like you have been here before. We started you off where you last saved.

        If you want to start a new game, use the `start` command.

        If you would like to resume another game, run the `resume` command with your given password. Or go to the URL that you were supplied.

        """

        datastore.temp_key = os.urandom(24).encode('hex')
        player = datastore.touch_player()

        if player:
            style_settings = style.get_settings(theme=player.theme, font=player.font)
        else:
            style_settings = style.get_settings()

        payload = {}
        payload['callback'] = [
            {
                'name': 'tempKey',
                'args': datastore.temp_key,
            }, {
                'name': 'load',
                'args': style_settings
            }
        ]

        if player is None:
            payload['console'] = utils.trim_docstring(new)
        else:
            payload['console'] = utils.trim_docstring(returning)

        return payload

    def start(self, *args):
        force = True if len(args) > 0 and args[0] == 'new' else False

        welcome = """
        You open your eyes. You're on the ground. You stand up and brush yourself off.

        "Where am I?" you wonder. "This place sure looks nebulous," your mind says.

        """

        player = datastore.get_player()

        if player is None:
            player = datastore.create_player()
        else:
            if force is False:
                prompt = """
                It looks like you already have a player.

                Are you sure you'd like to start over? If so, run `start new`.

                """
                return utils.trim_docstring(prompt)

        payload = {}
        payload['console'] = utils.trim_docstring(welcome)
        payload['callback'] = {
            'name': 'load',
            'args': style.get_settings(theme=player.theme, font=player.font)
        }

        return payload

    def color(self, theme='default'):
        """
        Change the color theme to an optional theme.

        Usage:
            color [<theme>]

        Options:
            default
            tomorrow
            cobalt
            espresso

        EXAMPLE:
            color tomorrow
                Changing color...

        NOTES:
            Leave off the theme to return to the default colors.
        """

        player = datastore.get_player()

        if player is None:
            return self.welcome()

        player.change_theme(theme)

        datastore.put_player(player)

        payload = {}
        payload['console'] = 'Changing color...'
        payload['callback'] = {
            'name': 'load',
            'args': style.get_settings(theme=theme, font=player.font)
        }

        return payload

    def font(self, font='monospace'):
        """
        Change the font to an optional font family.

        Usage:
            font [<family>]

        Options:
            sans-serif
            serif
            fantasy
            cursive
            monospace

        EXAMPLE:
            font cursive
                Changing font...

        NOTES:
            Leave off the family to return to the default font.
        """

        player = datastore.get_player()

        if player is None:
            return self.welcome()

        player.change_font(font)

        datastore.put_player(player)

        payload = {}
        payload['console'] = 'Changing font...'
        payload['callback'] = {
            'name': 'load',
            'args': style.get_settings(theme=player.theme, font=font)
        }

        return payload

    def save(self, *args):
        """
        Save your game.

        Usage:
            save

        Options:
            None

        EXAMPLE:
            save
                Will give details on how to resume your game in the future.
        """

        text = """
        Your game has been saved successfully.

        To play it again in the future, write down this code:
            {code}

        Then run it with the `resume` command like so:
            `resume {code}`
        """

        player = datastore.get_player()

        if player is None:
            return self.welcome()

        player.save()
        datastore.put_player(player)

        return utils.trim_docstring(text.format(code=player.player_id))

    def resume(self, *args):
        """
        Resume your past game.

        Usage:
            resume <code>

        Options:
            code       The code that was provided when saved.

        EXAMPLE:
            resume g65478asd1f35asg847
                Resuming game...

        """

        if len(args) != 1:
            return 'Invalid arguments. Please provide a resume code.'

        datastore.uid = args[0]

        player = datastore.get_player()

        if player is None:
            return 'Unable to find player with that code.'

        current_area = player.get_current_area()
        return current_area.description

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

        if player is None:
            return self.welcome()

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

        if player is None:
            return self.welcome()

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

        if player is None:
            return self.welcome()

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

        if player is None:
            return self.welcome()

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

        if player is None:
            return self.welcome()

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

        if player is None:
            return self.welcome()

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

        if player is None:
            return self.welcome()

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

        if player is None:
            return self.welcome()

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

        if player is None:
            return self.welcome()

        inventory = player.inventory()

        if len(inventory) == 0:
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

        if player is None:
            return self.welcome()

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

        if player is None:
            return self.welcome()

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

            link_cmd = '`{0}`'.format(cmd.lstrip())
            # We only want the description
            line = '\t{cmd}{desc}'.format(cmd=link_cmd.ljust(12),
                                          desc=help_str.split('\n')[1])

            result.append(line)

        return '\n'.join(result)

```

## base/game_controller.py

```python
from base.game import Game


class GameController(object):

    def __init__(self, uid, temp_key=None):
        self.uid = uid
        self.temp_key = temp_key

    def attack(self, name, item_name):
        return Game(self.uid, self.temp_key).attack(name, item_name)

    def look(self, direction=""):
        return Game(self.uid, self.temp_key).look(direction)

    def move(self, direction):
        return Game(self.uid, self.temp_key).move(direction)

    def examine(self, item_name):
        return Game(self.uid, self.temp_key).examine(item_name)

    def talk(self, char_name):
        return Game(self.uid, self.temp_key).talk(char_name)

    def eat(self, item_name):
        return Game(self.uid, self.temp_key).eat(item_name)

    def take(self, item_name):
        return Game(self.uid, self.temp_key).take(item_name)

    def put(self, item_name):
        return Game(self.uid, self.temp_key).put(item_name)

    def die(self):
        return Game(self.uid, self.temp_key).die()

    def use(self, item_name):
        return Game(self.uid, self.temp_key).use(item_name)

    def inventory(self):
        return Game(self.uid, self.temp_key).inventory()

    def help(self, command=None):
        return Game(self.uid, self.temp_key).help(command)

    def welcome(self):
        return Game(self.uid, self.temp_key).welcome()

    def start(self, *args):
        return Game(self.uid, self.temp_key).start(*args)

    def save(self, *args):
        return Game(self.uid, self.temp_key).save(*args)

    def resume(self, *args):
        return Game(self.uid, self.temp_key).resume(*args)

    def color(self, *args):
        return Game(self.uid, self.temp_key).color(*args)

    def font(self, *args):
        return Game(self.uid, self.temp_key).font(*args)

```

## base/style.py

```python
THEMES = {
    'default': {
        'body': 'hsla(210, 6.6667%, 11.7647%, 1)',
        'container': 'hsla(216, 6.1728%, 15.8824%, 1)',
    },
    'tomorrow': {
        'body': 'hsla(212, 92%, 20%, 1)',
        'container': 'hsla(210, 87%, 27%, 1)',
    },
    'cobalt': {
        'body': 'hsla(206, 92.5926%, 10.5882%, 1)',
        'container': 'hsla(206, 92.7711%, 16.2745%, 1)',
    },
    'espresso': {
        'body': 'hsla(23, 19.5652%, 18.0392%, 1)',
        'container': 'hsla(21, 12.7820%, 26.0784%, 1)',
    }
}

FONT = {
    'sans-serif': 'sans-serif',
    'serif': 'serif',
    'fantasy': 'fantasy',
    'cursive': 'cursive',
    'monospace': 'Monaco, Menlo, Consolas, "Courier New", monospace',
}


def get_theme(theme='default'):
    return THEMES.get(theme, {})


def get_font(font='monospace'):
    return FONT[font] if font in FONT else 'monospace'


def get_settings(theme='default', font='default'):
    return {
        'theme': get_theme(theme),
        'font': get_font(font),
    }

```

## base/urls.py

```python
from base import views as base_views


def apply_urls(app):
    app.add_url_rule('/', view_func=base_views.HomeView.as_view('home'))
    app.add_url_rule('/controller/', view_func=base_views.GameView.as_view('control'))

```

## base/utils.py

```python
import sys


def trim_docstring(docstring):
    """
    Trims a docstring to remove blank lines at the beginning and the end.

    Also removes any indentation from the beginning of the line in the
    docstring.

    Taken from PEP257: http://www.python.org/dev/peps/pep-0257/

    """

    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxint
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxint:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return '\n'.join(trimmed)

```

## base/views.py

```python
import json
import logging
import os

from flask import request, session

from flask.views import MethodView
from flask.templating import render_template

from base.game_controller import GameController


class HomeView(MethodView):
    def get(self):
        if 'uid' not in session:
            session['uid'] = os.urandom(24).encode('hex')

        return render_template('base.html')


class GameView(MethodView):
    def post(self):
        uid = session['uid']

        json_request = json.loads(request.data)
        raw_command = json_request.get('command', '')
        temp_key = json_request.get('tempKey', None)

        # Game to Map to
        game = GameController(uid, temp_key=temp_key)

        action_map = {
            'attack': game.attack,
            'die': game.die,
            'color': game.color,
            'eat': game.eat,
            'font': game.font,
            'examine': game.examine,
            'help': game.help,
            'inventory': game.inventory,
            'look': game.look,
            'move': game.move,
            'put': game.put,
            'resume': game.resume,
            'save': game.save,
            'start': game.start,
            'welcome': game.welcome,
            'take': game.take,
            'talk': game.talk,
            'use': game.use,
        }

        # Split up the command and assign to appropriate variables
        parts = raw_command.lower().split()

        if len(parts) == 0:
            return json.dumps({'console': 'I can\'t hear you, say it louder'})

        command = parts[0]
        args = parts[1:] if len(parts) > 1 else []

        action = action_map.get(command, None)

        if action is None:
            logging.info('Invalid command requested {0}'.format(command))
            result = 'That is an invalid command.'
        else:
            logging.info('Calling {0} with args: {1}'.format(command, ','.join(args)))
            result = action(*args)

        if type(result) == str or type(result) == unicode:
            payload = {
                'console': result,
            }
        else:
            payload = result

        return json.dumps(payload)

```

## base/world.py

```python
worlds = {}

default = worlds['default'] = {}

default['rooms'] = [
    {
        'name': 'room',
        'description': 'You see that your room is messy and a cat rolling around in a pile of socks...',
        'characters': ['cat'],
        'items': ['sock', 'sock', 'sock', 'sock'],
        'start': True,
        'connecting_areas': {
            'n': 'dungeon',
            's': 'dungeon',
            'e': 'dungeon',
            'w': 'dungeon',
        },
    },
    {
        'name': 'dungeon',
        'description': 'You see a dungeon... weird... why is that next to your room?',
        'characters': [],
        'items': [],
        'connecting_areas': {
            'n': 'room',
            's': 'room',
            'e': 'room',
            'w': 'room',
        },
    },
]

default['characters'] = [
    {
        'name': 'cat',
        'script': 'Meow...',
    },
]

default['items'] = [
    {
        'name': 'sock',
        'description': 'This is not any ordinary sock, it is a mysterious sock...',
        'use_reaction': 'The mysterious sock did nothing...',
        'eat_reaction': 'Whelp you just ate a sock... I hope you are proud...',
    },
]


def get_area(room_name=None, world_name='default'):
    world = worlds[world_name]

    if room_name is None:
        for room in world.get('rooms', []):
            if room.get('start', False) is True:
                return room
        return None
    else:
        for room in world.get('rooms', []):
            if room.get('name', '') == room_name:
                return room
        return None


def get_character(name, world_name='default'):
    world = worlds[world_name]

    for character in world.get('characters', []):
        if character.get('name', '') == name:
            return character

    return None


def get_item(name, world_name='default'):
    world = worlds[world_name]

    for item in world.get('items', []):
        if item.get('name', '') == name:
            return item

    return None

```

## base/models/__init__.py

```python
from .datastore import datastore
from .character import Character
from .area import Area
from .item import Item
from .player import Player

```

## base/models/area.py

```python
from base import world

from .datastore import datastore
from .player import Player

from google.appengine.ext import db


class Area(db.Model):
    name = db.StringProperty(required=True)
    description = db.StringProperty(required=True)
    current = db.BooleanProperty(default=False)
    temp_key = db.StringProperty()

    area_north = db.StringProperty()
    area_east = db.StringProperty()
    area_south = db.StringProperty()
    area_west = db.StringProperty()

    # Relational Properties
    player = db.ReferenceProperty(Player, collection_name='areas')

    @classmethod
    def new(cls, player, data, temp_key=None):
        area = cls(name=data['name'],
                   temp_key=temp_key,
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

    @classmethod
    def fetch(cls, temp_key, **kwargs):
        temp = cls.all().filter('temp_key', temp_key)
        saved = cls.all().filter('temp_key', None)

        for k, v in kwargs.iteritems():
            temp.filter(k, v)
            saved.filter(k, v)

        return temp.fetch(None) + saved.fetch(None)

    @classmethod
    def get(cls, temp_key, **kwargs):
        temp = cls.all().filter('temp_key', temp_key)
        saved = cls.all().filter('temp_key', None)

        for k, v in kwargs.iteritems():
            temp.filter(k, v)
            saved.filter(k, v)

        return temp.get() or saved.get()

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

        area = Area.get(self.temp_key, name=name, player=self.player)

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

```

## base/models/character.py

```python
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

    @classmethod
    def fetch(cls, temp_key, **kwargs):
        temp = cls.all().filter('temp_key', temp_key)
        saved = cls.all().filter('temp_key', None)

        for k, v in kwargs.iteritems():
            temp.filter(k, v)
            saved.filter(k, v)

        return temp.fetch(None) + saved.fetch(None)

    @classmethod
    def get(cls, temp_key, **kwargs):
        temp = cls.all().filter('temp_key', temp_key)
        saved = cls.all().filter('temp_key', None)

        for k, v in kwargs.iteritems():
            temp.filter(k, v)
            saved.filter(k, v)

        return temp.get() or saved.get()

    def attack(self, item):
        #TODO: Make attack do something
        return '{0} says: Ouch!'.format(self.name.capitalize())

    def get_name(self):
        return self.name

```

## base/models/datastore.py

```python
import logging

from base import world

from google.appengine.ext import db
from google.appengine.api import memcache


class DataStore(object):

    def __init__(self):
        self.uid = ''
        self.temp_key = None
        self.player = None

    def get_item_by_name(self, name):
        from base.models import Item

        data = world.get_item(name)

        if data is None:
            return None

        item = Item.new(data, temp_key=self.temp_key)

        return item

    def get_character_by_name(self, area, name):
        from base.models import Character

        data = world.get_character(name)

        if data is None:
            return None

        character = Character.new(area, data, temp_key=self.temp_key)

        return character

    def get_area_by_name(self, name=None):
        from base.models import Area

        area = Area.get(self.temp_key, name=name, player=self.player)

        if area is None:
            data = world.get_area(room_name=name)

            if data is None:
                return None

            area = Area.new(self.player, data, temp_key=self.temp_key)

        return area

    def save_game(self):
        from base import models

        for area in models.Area.all().filter('temp_key', self.temp_key).fetch(None):
            area.temp_key = None
            area.put()

        for item in models.Item.all().filter('temp_key', self.temp_key).fetch(None):
            item.temp_key = None
            item.put()

        for character in models.Character.all().filter('temp_key', self.temp_key).fetch(None):
            character.temp_key = None
            character.put()

    def put_player(self, player):
        player.put()

    def delete_player(self, player):
        db.delete(player)

    def put_area(self, area):
        area.put()

    def touch_player(self):
        logging.info('Touching player with %s', self.temp_key)
        player = self.get_player()

        if player is None:
            return None

        player.temp_key = self.temp_key
        player.put()
        return player

    def get_player(self):
        from base.models import Player

        player = Player.all().filter('player_id', self.uid).get()
        self.player = player

        return player

    def create_player(self):
        from base.models import Player
        return Player.new(self.uid, temp_key=self.temp_key)

datastore = DataStore()

```

## base/models/item.py

```python
from google.appengine.ext import db


class Item(db.Model):
    name = db.StringProperty()
    description = db.StringProperty()
    available = db.BooleanProperty(default=True)
    eat_reaction = db.StringProperty()
    use_reaction = db.StringProperty()
    temp_key = db.StringProperty()

    # Relational Attributes
    owner = db.ReferenceProperty(collection_name='items')

    @classmethod
    def new(cls, data, temp_key=None):
        item = cls(name=data['name'],
                   temp_key=temp_key,
                   description=data['description'],
                   eat_reaction=data['eat_reaction'],
                   use_reaction=data['use_reaction'])
        item.put()

        return item

    @classmethod
    def fetch(cls, temp_key, **kwargs):
        temp = cls.all().filter('temp_key', temp_key)
        saved = cls.all().filter('temp_key', None)

        for k, v in kwargs.iteritems():
            temp.filter(k, v)
            saved.filter(k, v)

        return temp.fetch(None) + saved.fetch(None)

    @classmethod
    def get(cls, temp_key, **kwargs):
        temp = cls.all().filter('temp_key', temp_key)
        saved = cls.all().filter('temp_key', None)

        for k, v in kwargs.iteritems():
            temp.filter(k, v)
            saved.filter(k, v)

        return temp.get() or saved.get()

```

## base/models/player.py

```python
import logging

from .datastore import datastore

from google.appengine.ext import db


class Player(db.Model):
    player_id = db.StringProperty(required=True)
    theme = db.StringProperty(default='default')
    font = db.StringProperty(default='monospace')
    current_area = db.ReferenceProperty()
    temp_key = db.StringProperty()

    @classmethod
    def new(cls, player_id, temp_key=None):
        player = cls(player_id=player_id,
                     temp_key=temp_key)
        player.put()

        return player

    def inventory(self):
        from base.models import Item

        return Item.fetch(self.temp_key, owner=self, available=True)

    def locations(self):
        from base.models import Area

        return Area.fetch(self.temp_key, player=self, available=True)

    def get_item(self, item_name):
        for item in self.inventory():
            if item.name == item_name:
                return item

        return None

    def change_theme(self, theme):
        self.theme = theme

    def change_font(self, font):
        self.font = font

    def add_item(self, item):
        if item is None:
            return

        item.owner = self
        item.put()

    def save(self):
        datastore.save_game()

    def get_current_area(self):
        if self.current_area is None:
            area = datastore.get_area_by_name()
            self.set_current_area(area)
        elif self.current_area.temp_key != self.temp_key:
            area = datastore.get_area_by_name(self.current_area.name)
            self.set_current_area(area)

        return self.current_area

    def set_current_area(self, area):
        self.current_area = area
        self.put()

    def use_item(self, item_name):
        item = self.get_item(item_name)

        if item is None:
            return 'You don\'t have that item in your inventory.'

        return item.use_reaction

    def eat_item(self, item_name):
        item = self.get_item(item_name)

        if item is None:
            return 'You don\'t have that item in your inventory.'

        item.available = False
        item.put()

        return item.eat_reaction

    def take_item(self, item_name):
        item = self.get_item(item_name)
        item.delete()

        return item

```

## css/base.css

```css
html, body, div, h1, h2, h3, h4, h5, h6, ul, ol, dl, li, dt, dd, p, blockquote, pre, form, fieldset, table, th, td { margin: 0; padding: 0; }
html, body {height: 100%;}
img { border: none; }
ul { list-style: none; }
a { text-decoration: none; }

body {
    font-family: Monaco, Menlo, Consolas, "Courier New", monospace;
    font-size: 14px;
    background-color: hsla(210, 6%, 12%, 1);
    color: hsla(180, 6%, 90%, 1);
    -webkit-transition: background-color 1000ms linear;
       -moz-transition: background-color 1000ms linear;
         -o-transition: background-color 1000ms linear;
            transition: background-color 1000ms linear;
}

/* We could make this webpage responsive o.O */

.container {
    width: 940px;
    height: 100%;
    margin: 0 auto;
    background-color: hsla(216, 6%, 16%, 1);
    overflow: hidden;
    position: relative;
    -webkit-transition: background-color 1000ms linear;
       -moz-transition: background-color 1000ms linear;
         -o-transition: background-color 1000ms linear;
            transition: background-color 1000ms linear;
}

.console {
    height: 100%;
    width: 960px;
    overflow-y: scroll;
    margin-bottom: -100px;
}

.console div.content {
    padding: 40px 50px;
    margin-bottom: 100px;
}

.console div.content > p, .console div.content > pre {
    font-family: Monaco, Menlo, Consolas, "Courier New", monospace;
    margin-bottom: 12px;
    font-size: 14px;
    white-space: pre-wrap;
}

.console pre a.command {
    color: #D87D50;
    border-bottom: 1px dashed #E4E7E7;
}

.orange {
    color: #D87D50;
}

.blue {
    color: #889AB4;
}

.light-yellow {
    color: #F9EE98;
}

.green {
    color: #8F9D6A;
}

.rust {
    color: #9B5C2E;
}

.red {
    color: #FF6400;
}

.purple {
    color: #9B859D;
}

.prompt {
    height: 60px;
    padding-bottom: 40px;
    width: 100%;
    background-color: #26282B;
    position: absolute;
    z-index: 1;
    -webkit-transition: background-color 1000ms linear;
       -moz-transition: background-color 1000ms linear;
         -o-transition: background-color 1000ms linear;
            transition: background-color 1000ms linear;
}

.prompt label {
    margin: 0 15px;
    font-size: 24px;
    padding: 10px;
    float: left;
}

.prompt a, .prompt span {
    color: #E4E7E7;
    margin: 0 15px;
    font-size: 24px;
    padding: 10px;
    float: left;
}

.prompt input {
    width: 790px;
    border: none;
    font-size: 24px;
    float: left;
    border: none;
    padding: 10px;

    -webkit-border-radius: 4px;
       -moz-border-radius: 4px;
            border-radius: 4px;
}

.prompt input:focus {
    border: none;
    outline: none;
}

```

## js/app.js

```javascript
'use strict';

/* Nebulous Adventure */


(function (root, $) {
    var $console = $('.console div.content'),
        $scroll = $('.console'),
        $prompt = $('.prompt'),
        $promptInput = $('#prompt'),
        $container = $('.container'),
        $body = $('body'),
        findCommands = function (text) {
            return text.replace(/`(.*)`/g, function (match, command) {
                return $('<div>').append($('<a>').addClass('command').attr('href', '#').text(command)).html();
            });
        },
        escape = function (text) {
            return text.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
        },
        command = function (text, hide) {
            var $indicator = $('.prompt label'),
                chars = '|/-\\',
                index = 0,
                requestFinished = false,
                time = 0,
                loader = setInterval(function () {
                    $indicator.text(chars[index]);

                    index = (index + 1) % chars.length;

                    if (requestFinished === true) {
                        $indicator.html('&gt;');
                        clearInterval(loader);
                    }
                }, 200),
                parts = text.split(' '),
                cmd = parts[0],
                tempKey = $('body').data('tempKey');

            if (!hide) {
                $('<pre>')
                    .text('> ' + text)
                    .appendTo($console);
            }

            if (cmd in localCommands) {
                var stop = localCommands[cmd]();
                requestFinished = true;
                if (stop) return;
            }

            $.ajax({
                url: '/controller/',
                type: 'POST',
                data: JSON.stringify({'command': text, 'tempKey': tempKey}),
                contentType: 'application/json',
                dataType: 'json'
            }).done(function(data){
                if('console' in data) {
                    reply(data.console);
                }
                if ('callback' in data) {
                    var list = [].concat(data.callback);
                    for(var i = 0; i < list.length; i++) {
                        var cb = list[i]['name'],
                            args = list[i]['args'];

                        callbacks[cb].apply(this, [].concat(args));
                    }
                }
                requestFinished = true;
                $promptInput.focus();
            });
        },
        reply = function (text) {
            var filtered = findCommands(escape(text));
            $('<pre>')
                .html(filtered)
                .appendTo($console);
            scrollConsole();
        },
        attachUnload = function () {
            $(window).on('beforeunload', function () {
                return 'Leaving Nebulous Adventure will cause you to lose all your unsaved progress.'
            });
        },
        removeUnload = function() {
            $(window).off('beforeunload');
        },
        scrollConsole = function () {
            $scroll.get(0).scrollTop = $scroll.get(0).scrollHeight;
        },
        resetPrompt = function () {
            $promptInput.val('');
            scrollConsole();
        },
        clearCommand = function () {
            $console.html('');
            return true;
        },
        startCommand = function () {
            clearCommand();
        },
        localCommands = {
            'clear': clearCommand,
        },
        tempKeyCallback = function (key) {
            console.log('Temp key callback');
            $('body').data('tempKey', key);
            attachUnload();
        },
        loadCallback = function (settings) {
            console.log('Loading callback');
            console.log(settings);
            if (settings.theme) {
                $body.css('backgroundColor', settings.theme.body);
                $container.css('backgroundColor', settings.theme.container);
                $prompt.css('backgroundColor', settings.theme.container);
            }
            if (settings.font) {
                $('.console div.content > pre').css('fontFamily', settings.font)
            }
            scrollConsole();
        },
        callbacks = {
            'tempKey': tempKeyCallback,
            'load': loadCallback,
        };

    // Focus prompt on load
    $(document).ready(function () {
        $promptInput.focus();
        command('welcome', true);
    });

    // Add a submit handler
    $('.prompt form').submit(function () {
        var val = $promptInput.val();
        resetPrompt();
        command(val);
        return false;
    });

    // Show help
    $('.prompt a').on('click', function () {
        command('help');
    });

    $('.console').on('click', 'a.command', function (e) {
        var $this = $(this);

        command($this.text());
        e.preventDefault();
    });
}(window, jQuery));

```

## templates/base.html

```html
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <title>Nebulous Adventure</title>
    <link rel="stylesheet" href="/css/base.css" type="text/css" media="all" />
    <link rel="icon" href="/img/favicon.ico" />
</head>
<body>
<div class="container">
    <div class="console">
        <div class="content">
        </div>
    </div>
    <div class="prompt">
        <form action="GET">
            <label for="prompt">&gt;</label>
            <input type="text" name="c" id="prompt" value="" />
            <a href="#">?</a>
        </form>
    </div>

    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>
    <script src="/js/app.js" type="text/javascript" charset="utf-8"></script>
</div>
</body>
</html>

```
