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
