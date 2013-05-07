Diagram Fragments
=================

## GameController
* s = save():String
* s = resume(key:String):String
* b = change\_colors(theme:String):Boolean
* b = change\_font(font:String):Boolean

## Game
* s = save():String
* s = resume(key:String):String
* b = change\_colors(theme:String):Boolean
* b = change\_font(font:String):Boolean

## Player
* a = current\_area():Area
* s = save():String
* change\_theme(theme:String)
* change\_font(font:String)

## Area
* s = description():String

## DataStore
* p = get\_player():Player
* b = put\_player(p:Player):Boolean
