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

