
# Source Code for Nebulous Adventure


## /Users/joshuad/Downloads/nebulous-adventure-master/main.py

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

## /Users/joshuad/Downloads/nebulous-adventure-master/base/__init__.py

```python

```

## /Users/joshuad/Downloads/nebulous-adventure-master/base/actions.py

```python

```

## /Users/joshuad/Downloads/nebulous-adventure-master/base/models.py

```python
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
            north  	Room to the north
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

```

## /Users/joshuad/Downloads/nebulous-adventure-master/base/urls.py

```python
from base import views as base_views


def apply_urls(app):
    app.add_url_rule('/', view_func=base_views.HomeView.as_view('home'))
    app.add_url_rule('/controller/', view_func=base_views.GameController.as_view('control'))


```

## /Users/joshuad/Downloads/nebulous-adventure-master/base/utils.py

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


class GameData(object):
    world_map = {
        'start' : {'connecting_areas':{'n':'dungeon', 's':'dungeon', 'e':'dungeon', 'w':'dungeon'},
                   'description':'You see that your room is messy and a cat rolling around in a pile of socks...',
                   'characters':['Cat']},

        'dungeon' : {'connecting_areas':{'n':'start', 's':'start', 'e':'start', 'w':'start'},
                   'description':'You see a dungeon... weird... why is that next to your room?',
                   'characters':[]}
    }

    characters = {
        'Cat':{'script':'Meow...'}
    }

    items = {
        'Sock':{'description': 'This is not any ordinary sock, it is a mysterious sock...'}
    }

def check_map(area, direction):
    local_area = GameData().world_map.get(area.get_name())
    if local_area is not None:
        connecting_area_id = local_area.get('connecting_areas').get(direction)
        if connecting_area_id is not None:
            from base.models import DataStore
            return DataStore().get_area_by_name(connecting_area_id)
    return None

def generate_test_data(erase_reset=True):
    from google.appengine.ext import db
    from base import models
    print 'Generating Game Data...'
    if erase_reset:

        to_delete = []
        to_delete.extend(models.Character.all(keys_only=True).fetch(None))
        to_delete.extend(models.Item.all(keys_only=True).fetch(None))
        to_delete.extend(models.Area.all(keys_only=True).fetch(None))
        to_delete.extend(models.Player.all(keys_only=True).fetch(None))
        db.delete(to_delete)
        print '\n(Deleted old data...)\n'

    to_put = []
    print 'Characters'
    for key, character in GameData().characters.iteritems():
        new_character = models.Character(name = key,
                                         script = character['script'])
        print '********'
        print '  name: %s\n  script: %s'%(new_character.name, new_character.script)

        to_put.append(new_character)
    print '********'

    print '\nItems'
    for key, item in GameData().items.iteritems():
        new_item = models.Item(name = key,
                               description = item['description'])
        print '********'
        print '  name: %s\n  description: %s'%(new_item.name, new_item.description)
        to_put.append(new_item)
    print '********'

    print '\nAreas'
    for key, area in GameData().world_map.iteritems():
        new_area = models.Area(name = key,
                               description = area.get('description'),
                               characters = area.get('characters'))
        print '********'
        print '  name: %s\n  description: %s\n  characters: %s'%(new_area.name, new_area.description, new_area.characters)
        to_put.append(new_area)
    print '********'
    db.put(to_put)


```

## /Users/joshuad/Downloads/nebulous-adventure-master/base/views.py

```python
import json
import logging
import os

from flask import request, session

from flask.views import MethodView
from flask.templating import render_template

from base import models

# Game to Map to
game = models.Game()

action_map = {
    'eat': game.eat,
    'examine': game.examine,
    'look': game.look,
    'move': game.move,
    'talk': game.talk,
    'help': game.help,
}


class HomeView(MethodView):
    def get(self):
        if 'uid' not in session:
            session['uid'] = os.urandom(24)

        return render_template('base.html')


class GameController(MethodView):
    def get(self):
        return json.dumps(action_map.keys())

    def post(self):
        if 'uid' not in session:
            session['uid'] = os.urandom(24)

        uid = session['uid'].encode('hex')

        json_request = json.loads(request.data)
        raw_command = json_request.get('command', '')

        # Split up the command and assign to appropriate variables
        parts = raw_command.split()

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
            try:
                result = action(uid, *args)
            except TypeError, e:
                logging.error('Got error {0}'.format(e))
                logging.info('Not enough arguments given for command {0}'.format(command))
                result = 'Not enough arguments given.'

        return json.dumps({'console': result})

```

## /Users/joshuad/Downloads/nebulous-adventure-master/css/base.css

```css
html, body, div, h1, h2, h3, h4, h5, h6, ul, ol, dl, li, dt, dd, p, blockquote, pre, form, fieldset, table, th, td { margin: 0; padding: 0; }
html, body {height: 100%;}
img { border: none; }
ul { list-style: none; }
a { text-decoration: none; }

body {
    font-family: Monaco, Menlo, Consolas, "Courier New", monospace;
    font-size: 14px;
    background-color: #1d1f21;
    color: #E4E7E7;
}

/* We could make this webpage responsive o.O */

.container {
    width: 940px;
    height: 100%;
    margin: 0 auto;
    background-color: #26282B;
    overflow: hidden;
    position: relative;
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

## /Users/joshuad/Downloads/nebulous-adventure-master/js/app.js

```javascript
'use strict';

/* Nebulous Adventure */


(function (root, $) {

    var $console = $('.console div.content'),
        $scroll = $('.console'),
        $prompt = $('#prompt'),
        command = function (text) {
            $('<pre>')
                .text('> ' + text)
                .appendTo($console);
        },
        reply = function (text) {
            $('<pre>')
                .text(text)
                .appendTo($console);
        },
        resetPrompt = function () {
            $prompt.val('');
            $scroll.get(0).scrollTop = $scroll.get(0).scrollHeight;
        };

    // Focus prompt on load
    $(document).ready(function () {
        $prompt.focus();
    });

    // Add a submit handler
    $('.prompt form').submit(function () {
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
            }, 200);

        command($prompt.val());

        $.ajax({
            url: '/controller/',
            type: 'POST',
            data: JSON.stringify({'command': $prompt.val()}),
            contentType: 'application/json',
            dataType: 'json'
        }).done(function(data){
            if(data.hasOwnProperty("console")) {
                reply(data.console);
                requestFinished = true;
            }
            resetPrompt();
        });

        return false;
    });
    // Show help
    $('.prompt a').on('click', function () {
        command('help');

        $.ajax({
            url: '/controller/',
            type: 'POST',
            data: JSON.stringify({'command': 'help'}),
            contentType: 'application/json',
            dataType: 'json'
        }).done(function(data){
            if(data.hasOwnProperty("console")) {
                reply(data.console);
            }
            resetPrompt();
        });
    });
}(window, jQuery));

```

## /Users/joshuad/Downloads/nebulous-adventure-master/scripts/concat.py

```python
import os
import sys

src_dir = os.getcwd()

languages = {
	'.py': 'python',
	'.js': 'javascript',
	'.html': 'html',
	'.css': 'css',
}

exclude_dirs = [
	os.path.join(src_dir, 'flask'),
	os.path.join(src_dir, 'werkzeug'),
]

def writeHeader(output):
	output.write('\n')
	output.write('# Source Code for Nebulous Adventure')
	output.write('\n\n')

def writeSource(output, file, lang):
	print 'Writing source!'
	# Write Markdown header info
	output.write('\n')
	output.write('## {0}'.format(file))
	output.write('\n\n')
	
	# Write GitHub flavored Markdown info
	output.write('```{0}'.format(lang))
	output.write('\n')
	
	# Write file source
	src_file = open(file)
	output.writelines(src_file.xreadlines())
	
	output.write('\n')
	output.write('```')
	output.write('\n')
	

def visit(output, dirname, files):
	print 'Visiting {0}'.format(dirname)
	
	prefix = ''
	for exclude in exclude_dirs:
		prefix = os.path.commonprefix((exclude, dirname))
		if prefix == exclude:
			return

	if dirname in exclude_dirs:
		return
	
	for file in files:
		print 'Iterating with file: {0}'.format(file)
		root, ext = os.path.splitext(file)
		
		if ext in languages:
			lang = languages[ext]
			file_path = os.path.join(dirname, file)
			writeSource(output, file_path, lang)
			
def main(args):
	output = open(os.path.join(src_dir, 'SOURCE.md'), 'w')
	writeHeader(output)
	
	# Well this function is short =]
	os.path.walk(src_dir, visit, output)
	
	output.close()
	
	return 0

	
if __name__ == '__main__':
	sys.exit(main(sys.argv))
```

## /Users/joshuad/Downloads/nebulous-adventure-master/templates/base.html

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
            <p>
                There is a fifth dimension beyond that which is known to man.
            </p>
            <p>
                It is a dimension as vast as space and as timeless as infinity.
            </p>
            <p>
                It is the middle ground between light and shadow, between science and superstition, and it lies between the pit of man's fears and the summit of his knowledge.
            </p>
            <p>
                This is the dimension of imagination. It is a journey which we call "<span class="orange">The Nebulous Adventure</span>".
            </p>
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
