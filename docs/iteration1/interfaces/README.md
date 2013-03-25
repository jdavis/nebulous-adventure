Java Interfaces
===============

## Game Interface
```java

import java.util.List;

public interface GameInterface {
    public String look(String uid, String direction);
    public String move(String uid, String direction);
    public String examine(String uid, String name);
    public String talk(String uid, String name);
    public String eat(String uid, String item);
}

```

## Player Interface
```java

import java.util.List;

public interface PlayerInterface {
    public List<Item> getAllItems();
    public Player getPlayer(String id);
    public Area getDirection(String direction);
    public Area getCurrentArea();
    public Boolean setArea(Area a);
    public Item getItem(String name);
    public String eatItem(String name);
}

```

## Character Interface
```java

import java.util.List;

public interface CharacterInterface {
    public List<Character> getCharacter(String name);
    public String talk();
}

```

## DataStore Interface
```java

import java.util.List;

public interface DataStoreInterface {
    public Area getArea(String id);
    public Player getPlayer(String id);
    public Item getItem(String name);
    public List<Character> getCharacters(String name);
}

```


## Area Interface
```java

import java.util.List;

public interface AreaInterface {
    public String getDescription();
    public List<Item> getAllItems();
    public Area getDirection(String direction);
    public Character getCharacter(String name);
    public String look(String direction);
    public String talkTo(String name);
}

```


## Item Interface
```java

import java.util.List;

public interface ItemInterface {
    public String getDescription();
    public List<Item> getItems();
    public String eatItem();
}

```

