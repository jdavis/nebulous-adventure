Java Interfaces
===============

## Game
* s = look(d: String):String
* s = move(d: String):String
* s = examine(i: String):String
* s = talk(n: String):String
* s = eat(i: String):String
 
## Player
*  getAllItems():List
* public Player getPlayer(String id);
* a = getDirection(d: String):Area
* a = getCurrentArea():Area
* s = setArea(a: Area):Boolean
* i = getItem(name: String):Item
* s = eatItem(name: String):String
 
## Character
* l = getCharacter(name: String):List
* s = talk():String
 
## DataStore
* a = getArea(id: String):Area
* p = getPlayer(id: String):Player
* i = getItem(name: Player):Item
* l = getCharacters(name: String):List
 
## Area
* s = getDescription():String
* l = getAllItems():List
* a = getDirection(d: String):Area
* c = getCharacter(name: String):Character
* s = look(d: String):String
* s = talkTo(n: String):String
 
## Item
* s = getDescription():String
* l = getItems():List
* s = eatItem():String
