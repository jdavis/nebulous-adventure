Java Interfaces
===============

## GameController Interface
```java

import java.util.List;

public interface GameControllerInterface {
    public String take(String item, String id);
    public String put(String item, String id);
    public String use(String item, String id);
    public String die(String item, String id);
    public String attack(String name, String item, String id);
}

```

## Game Interface
```java

import java.util.List;

public interface GameInterface {
    public String take(String item, String id);
    public String put(String item, String id);
    public String use(String item, String id);
    public String die(String item, String id);
    public String attack(String name, String item, String id);
}

```

## Player Interface
```java

import java.util.List;

public interface PlayerInterface {
    public Area getArea();
    public String addItem(Item i);
    public Item getItem(String n);
    public Item takeItem(String n);
    public String useItem(String n);
}

```

## Character Interface
```java

import java.util.List;

public interface CharacterInterface {
    public String attack(Item i);
}

```

## Area Interface
```java

import java.util.List;

public interface AreaInterface {
    public Item takeItem(String n);
    public String putItem(Item i);
    public String attack(String n, Item i):
}

```


## Item Interface
```java

import java.util.List;

public interface ItemInterface {
    public String use();
}

```

## DataStore Interface
```java

import java.util.List;

public interface DataStoreInterface {
    public Area getArea(String id);
    public boolean putArea(Area a);
    public Player getPlayer(String id);
    pubic boolean putPlayer(Player p);
    public boolean removePlayer(String id);
    public Item getItemByName(String n);
    public Character getCharacterByName(String n);
    public boolean putCharacter(Character c);
}

```
