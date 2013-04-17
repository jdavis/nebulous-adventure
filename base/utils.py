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
                   'characters':['cat'],
                   'items':['sock', 'sock', 'sock', 'sock']},

        'dungeon' : {'connecting_areas':{'n':'start', 's':'start', 'e':'start', 'w':'start'},
                   'description':'You see a dungeon... weird... why is that next to your room?',
                   'characters':[],
                   'items':[]},
    }

    characters = {
        'cat':{'script':'Meow...'},
    }

    items = {
        'sock':{'description': 'This is not any ordinary sock, it is a mysterious sock...',
                'use_reaction': 'The mysterious sock did nothing...',
                'eat_reaction': 'Whelp you just ate a sock... I hope you are proud...'},
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
                               description = item['description'],
                               use_reaction = item['use_reaction'],
                               eat_reaction = item['eat_reaction'])
        print '********'
        print '  name: %s\n  description: %s'%(new_item.name, new_item.description)
        to_put.append(new_item)
    print '********'

    print '\nAreas'
    for key, area in GameData().world_map.iteritems():
        new_area = models.Area(name = key,
                               description = area.get('description'),
                               characters = area.get('characters'),
                               items = area.get('items'))
        print '********'
        print '  name: %s\n  description: %s\n  characters: %s\n  items: %s'%(new_area.name, new_area.description, new_area.characters, new_area.items)
        to_put.append(new_area)
    print '********'
    db.put(to_put)

