Diagram Fragments 
=================

## GameController
* s = welcome():String
* s = start(key:String):String


## Game
* s = welcome():String
* s = start(key:String):String


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
