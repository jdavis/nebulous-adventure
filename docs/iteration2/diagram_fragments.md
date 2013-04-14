Diagram Fragments 
=================

## GameController
* s = take(i: String, id: String):String
* s = put(i: String, id: String):String
* s = use(i: String, id: String):String
* s = die(i: String, id: String):String
* s = attack(i: String, id: String):String

## Game
* s = take(i: String, id: String):String
* s = put(i: String, id: String):String
* s = use(i: String, id: String):String
* s = die(i: String, id: String):String
* s = attack(i: String, id: String):String

## Player
* ca = getArea():Area
* s = addItem(i: Item):String
* i = getItem(n: String):Item
* i = takeItem(n: String):Item
* s = useItem(n: String):String

## Item
* s = use():String

## Area
* i = takeItem(n: String):Item
* s = putItem(i: Item):String
* s = attack(n: String, i: Item):String

## Character
* s = attack(i: Item):String

## DataStore
* ca = getArea(id: String):Area
* b = putArea(a: Area):Boolean
* p = getPlayer(id: String):Player
* b = putPlayer(p: Player):Boolean
* b = removePlayer(id: String):Boolean
* i = getItemByName(n: String):Item
* c = getCharacterByName(n: String):Character
* b = putCharacter(c: Character):Boolean
